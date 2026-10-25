"""Print machine facts that take more than one shell command to find.

Works on Windows, WSL, and other Linux, and prints compact JSON.
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WINDOWS = "windows"
WSL = "wsl"
LINUX = "linux"


def detect_platform() -> str:
    if sys.platform == "win32":
        return WINDOWS
    if "microsoft" in platform.release().lower():
        return WSL
    return sys.platform


PLATFORM = detect_platform()
ON_WINDOWS = PLATFORM == WINDOWS
HOME = Path.home()
GIB = 1024**3

# Display adapters. Reading the registry avoids a PowerShell CIM query,
# which takes about a second to start.
DISPLAY_CLASS = (
    r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
)


def run(*command: str, encoding: str = "utf-8") -> str | None:
    """Return the stripped stdout of a command, or None when it fails."""
    try:
        result = subprocess.run(command, capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode(encoding, errors="replace").strip()


def gib(size: int) -> float:
    return round(size / GIB, 1)


def env_path(variable: str, default: Path) -> Path:
    return Path(os.environ.get(variable) or default)


def existing(path: Path) -> str | None:
    return str(path) if path.exists() else None


def registry_value(key: str, name: str) -> object | None:
    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as handle:
            return winreg.QueryValueEx(handle, name)[0]
    except OSError:
        return None


# machine


def os_name() -> str:
    if ON_WINDOWS:
        return f"Windows {platform.release()} {platform.version()}"
    try:
        return platform.freedesktop_os_release()["PRETTY_NAME"]
    except (OSError, KeyError):
        return f"{platform.system()} {platform.release()}"


def cpu_name() -> str | None:
    if ON_WINDOWS:
        key = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        name = registry_value(key, "ProcessorNameString")
        return str(name).strip() if name else None
    try:
        cpuinfo = Path("/proc/cpuinfo").read_text()
    except OSError:
        return None
    match = re.search(r"^model name\s*:\s*(.+)$", cpuinfo, re.MULTILINE)
    return match[1].strip() if match else None


def memory_bytes() -> int | None:
    if ON_WINDOWS:
        import ctypes

        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_ulong),
                ("load", ctypes.c_ulong),
                ("total_physical", ctypes.c_ulonglong),
                ("avail_physical", ctypes.c_ulonglong),
                ("total_page", ctypes.c_ulonglong),
                ("avail_page", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong),
                ("avail_virtual", ctypes.c_ulonglong),
                ("avail_extended", ctypes.c_ulonglong),
            ]

        status = MemoryStatus(length=ctypes.sizeof(MemoryStatus))
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return None
        return status.total_physical
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except (ValueError, OSError):
        return None


def gpus() -> list[str]:
    if ON_WINDOWS:
        import winreg

        names = []
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, DISPLAY_CLASS) as root:
            for index in range(winreg.QueryInfoKey(root)[0]):
                try:
                    with winreg.OpenKey(root, winreg.EnumKey(root, index)) as adapter:
                        names.append(winreg.QueryValueEx(adapter, "DriverDesc")[0])
                except OSError:
                    continue  # The Properties subkey denies access.
        return names
    if PLATFORM == WSL:
        # WSL reads the Windows host registry through interop.
        key = rf"HKLM\{DISPLAY_CLASS}"
        output = run("reg.exe", "query", key, "/s", "/v", "DriverDesc") or ""
        pattern = re.compile(r"DriverDesc\s+REG_SZ\s+(.+)")
        return [m[1].strip() for m in map(pattern.search, output.splitlines()) if m]
    output = run("lspci") or ""
    return [line for line in output.splitlines() if "VGA" in line or "3D" in line]


def wsl_info() -> dict | None:
    if ON_WINDOWS:
        # wsl.exe prints UTF-16 regardless of the console code page.
        output = run("wsl", "--list", "--quiet", encoding="utf-16-le") or ""
        return {
            "distros": [line.strip() for line in output.splitlines() if line.strip()]
        }
    if PLATFORM == WSL:
        return {
            "distro": os.environ.get("WSL_DISTRO_NAME"),
            "windows_interop": shutil.which("cmd.exe") is not None,
        }
    return None


def machine_section() -> dict:
    memory = memory_bytes()
    info = {
        "platform": PLATFORM,
        "os": os_name(),
        "cpu": cpu_name(),
        "cores": os.cpu_count(),
        "memory_gib": gib(memory) if memory else None,
        "gpus": gpus(),
        "wsl": wsl_info(),
    }
    if PLATFORM == WSL:
        info["note"] = (
            "Cores and memory are WSL VM limits. GPUs are the Windows host's."
        )
    return info


# paths


def uv_paths() -> dict | None:
    if shutil.which("uv") is None:
        return None
    return {
        "bin": run("uv", "tool", "dir", "--bin"),
        "tools": run("uv", "tool", "dir"),
        "python": run("uv", "python", "dir"),
        "cache": run("uv", "cache", "dir"),
    }


def pixi_info() -> dict | None:
    output = run("pixi", "info", "--json")
    return json.loads(output) if output else None


def pixi_paths(info: dict | None) -> dict | None:
    if info is None:
        return None
    global_info = info.get("global_info") or {}
    return {
        "bin": global_info.get("bin_dir"),
        "envs": global_info.get("env_dir"),
        "cache": info.get("cache_dir"),
    }


def cargo_paths() -> dict | None:
    if shutil.which("cargo") is None:
        return None
    home = env_path("CARGO_HOME", HOME / ".cargo")
    return {
        "bin": str(home / "bin"),
        "registry_src": existing(home / "registry" / "src"),
        "git_checkouts": existing(home / "git" / "checkouts"),
        "rustup_toolchains": existing(
            env_path("RUSTUP_HOME", HOME / ".rustup") / "toolchains"
        ),
    }


def bun_paths() -> dict | None:
    if shutil.which("bun") is None:
        return None
    home = env_path("BUN_INSTALL", HOME / ".bun")
    return {
        "bin": run("bun", "pm", "bin", "--global"),
        "global_modules": existing(home / "install" / "global" / "node_modules"),
        "cache": run("bun", "pm", "cache"),
    }


def paths_section() -> dict:
    return {
        "uv": uv_paths(),
        "pixi": pixi_paths(pixi_info()),
        "cargo": cargo_paths(),
        "bun": bun_paths(),
    }


# packages


def parse_versions(output: str | None, pattern: str) -> dict | None:
    if output is None:
        return None
    regex = re.compile(pattern)
    return dict(m.groups() for m in map(regex.search, output.splitlines()) if m)


def pixi_packages() -> dict | None:
    manifest = ((pixi_info() or {}).get("global_info") or {}).get("manifest")
    if manifest is None:
        return None
    try:
        envs = tomllib.loads(Path(manifest).read_text(encoding="utf-8")).get("envs", {})
    except (OSError, tomllib.TOMLDecodeError):
        return None
    # An environment name may differ from its commands, such as rg in shell-tools.
    return {name: sorted(env.get("exposed", {})) for name, env in envs.items()}


def packages_section() -> dict:
    return {
        "pixi": pixi_packages(),
        # "ruff v0.17.2", followed by "- ruff" lines.
        "uv": parse_versions(run("uv", "tool", "list"), r"^(\S+) v(\S+)$"),
        # "tokei v15.0.0:", followed by indented binaries.
        "cargo": parse_versions(
            run("cargo", "install", "--list"), r"^(\S+) v([^\s:]+)(?: \(.*\))?:$"
        ),
        # A tree line such as "+-- @scope/name@1.2.3". The first line is a header.
        "bun": parse_versions(
            run("bun", "pm", "ls", "--global"), r"(?<=\s)(@?[^\s@]+)@(\S+)$"
        ),
    }


# disk


def filesystem(root: str) -> str | None:
    import ctypes

    name = ctypes.create_unicode_buffer(32)
    ok = ctypes.windll.kernel32.GetVolumeInformationW(
        root, None, 0, None, None, None, name, len(name)
    )
    return name.value if ok else None


def volume(path: str) -> dict | None:
    try:
        total, _, free = shutil.disk_usage(path)
    except OSError:
        return None  # An empty card reader or optical drive has no size.
    return {"path": path, "total_gib": gib(total), "free_gib": gib(free)}


def disk_section() -> dict:
    if ON_WINDOWS:
        volumes = []
        for root in os.listdrives():
            if info := volume(root):
                # A Dev Drive is a ReFS volume.
                volumes.append(info | {"dev_drive": filesystem(root) == "ReFS"})
        key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock"
        developer_mode = registry_value(key, "AllowDevelopmentWithoutDevLicense") == 1
        # Without Developer Mode, symbolic links need an elevated shell.
        link = "symlink" if developer_mode else "junction"
        return {"volumes": volumes, "preferred_link": link}

    paths = [str(HOME)]
    if PLATFORM == WSL:
        paths += sorted(str(p) for p in Path("/mnt").glob("[a-z]"))
    info: dict = {"volumes": [v for v in map(volume, paths) if v]}
    if PLATFORM == WSL:
        info["note"] = (
            "The Linux disk is virtual and reports its maximum size."
            " /mnt/<drive> shows the Windows drives behind it."
        )
    return info


SECTIONS: dict[str, tuple[Callable[[], dict], str]] = {
    "machine": (machine_section, "platform, OS, CPU, cores, memory, GPUs, and WSL"),
    "paths": (
        paths_section,
        "bin, package source, and cache dirs of uv, pixi, cargo, bun",
    ),
    "packages": (packages_section, "global packages of pixi, uv, cargo, and bun"),
    "disk": (disk_section, "volume sizes, Dev Drives, and the preferred link type"),
}


def render(value: object, depth: int = 0) -> str:
    """Format JSON with one line per item instead of one line per value."""
    flat = json.dumps(value, ensure_ascii=False)
    if not isinstance(value, dict | list) or not value:
        return flat
    if depth >= 3 or (depth == 2 and len(flat) <= 100):
        return flat
    pad = "  " * (depth + 1)
    if isinstance(value, dict):
        items = [
            f"{pad}{json.dumps(k)}: {render(v, depth + 1)}" for k, v in value.items()
        ]
        brackets = "{}"
    else:
        items = [pad + render(v, depth + 1) for v in value]
        brackets = "[]"
    body = ",\n".join(items)
    return f"{brackets[0]}\n{body}\n{'  ' * depth}{brackets[1]}"


def main() -> None:
    sections = "\n".join(f"  {name:<10}{help}" for name, (_, help) in SECTIONS.items())
    parser = argparse.ArgumentParser(
        prog="sysinfo.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"sections:\n{sections}\n\n"
            "examples:\n"
            "  uv run python sysinfo.py machine\n"
            "  uv run python sysinfo.py paths packages"
        ),
    )
    parser.add_argument(
        "sections", nargs="*", metavar="section", help="sections to print"
    )
    names = parser.parse_args().sections
    if not names:
        parser.print_help()
        return
    unknown = [name for name in names if name not in SECTIONS]
    if unknown:
        parser.error(
            f"unknown section {', '.join(unknown)}, choose from {', '.join(SECTIONS)}"
        )
    with ThreadPoolExecutor() as pool:
        results = pool.map(lambda name: SECTIONS[name][0](), names)
        print(render(dict(zip(names, results, strict=True))))


if __name__ == "__main__":
    main()
