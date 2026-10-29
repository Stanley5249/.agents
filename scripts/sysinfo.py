# /// script
# requires-python = ">=3.12"
# ///
"""Print environment and machine facts as UTF-8 JSON.

Requires Python 3.12+. Environment facts describe this Python process.
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WINDOWS = "windows"
WSL = "wsl"


def detect_platform() -> str:
    if sys.platform == "win32":
        return WINDOWS
    if "microsoft" in platform.release().lower():
        return WSL
    return sys.platform


PLATFORM = detect_platform()
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


# environment


def environment_section() -> dict:
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "home": str(Path.home()),
    }
    if distro := os.environ.get("WSL_DISTRO_NAME"):
        info["WSL_DISTRO_NAME"] = distro
    return info


# machine


def os_name() -> str:
    if PLATFORM == WINDOWS:
        return f"Windows {platform.release()} {platform.version()}"
    try:
        return platform.freedesktop_os_release()["PRETTY_NAME"]
    except (OSError, KeyError):
        return f"{platform.system()} {platform.release()}"


def cpu_name() -> str | None:
    if PLATFORM == WINDOWS:
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
    if PLATFORM == WINDOWS:
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


def gpus() -> list[str] | None:
    if PLATFORM == WINDOWS:
        import winreg

        names = []
        try:
            root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, DISPLAY_CLASS)
        except OSError:
            return None
        with root:
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
        output = run("reg.exe", "query", key, "/s", "/v", "DriverDesc")
        if output is None:
            return None
        pattern = re.compile(r"DriverDesc\s+REG_SZ\s+(.+)")
        return [m[1].strip() for m in map(pattern.search, output.splitlines()) if m]
    output = run("lspci")
    if output is None:
        return None
    return [line for line in output.splitlines() if "VGA" in line or "3D" in line]


def wsl_distros() -> list[str] | None:
    """List the installed distros. Inside WSL, the platform field already says so."""
    if PLATFORM != WINDOWS:
        return None
    # wsl.exe prints UTF-16 regardless of the console code page.
    output = run("wsl", "--list", "--quiet", encoding="utf-16-le")
    if output is None:
        return None
    return [line.strip() for line in output.splitlines() if line.strip()]


def machine_section() -> dict:
    memory = memory_bytes()
    info = {
        "platform": PLATFORM,
        "os": os_name(),
        "cpu": cpu_name(),
        "cores": os.cpu_count(),
        "memory_gib": gib(memory) if memory else None,
        "gpus": gpus(),
        "wsl_distros": wsl_distros(),
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


def pixi_paths() -> dict | None:
    output = run("pixi", "info", "--json")
    if output is None:
        return None
    try:
        info = json.loads(output)
    except json.JSONDecodeError:
        return None  # Invalid tool output is unavailable data, like a failed command.
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
        "cache": existing(home / "install" / "cache"),
    }


def paths_section() -> dict:
    return {
        "uv": uv_paths(),
        "pixi": pixi_paths(),
        "cargo": cargo_paths(),
        "bun": bun_paths(),
    }


# packages


def output_lines(*command: str) -> list[str] | None:
    output = run(*command)
    return None if output is None else output.splitlines()


def packages_section() -> dict:
    # The list formats differ per tool, so the raw lines are the data.
    return {
        "pixi": output_lines("pixi", "global", "list"),
        "uv": output_lines("uv", "tool", "list"),
        "cargo": output_lines("cargo", "install", "--list"),
        "bun": output_lines("bun", "pm", "ls", "--global"),
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
    if PLATFORM == WINDOWS:
        volumes = []
        for root in os.listdrives():
            if info := volume(root):
                # A Dev Drive is ReFS, but not every ReFS volume is a Dev Drive.
                volumes.append(info | {"filesystem": filesystem(root)})
        key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock"
        developer_mode = registry_value(key, "AllowDevelopmentWithoutDevLicense") == 1
        # Without Developer Mode, symbolic links need an elevated shell.
        return {"volumes": volumes, "developer_mode": developer_mode}

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
    "environment": (
        environment_section,
        "process OS, kernel release, architecture, home, and WSL distro when present",
    ),
    "machine": (
        machine_section,
        "platform, OS, CPU, cores, memory, GPUs, and WSL distros",
    ),
    "paths": (
        paths_section,
        "bin, package source, and cache dirs of uv, pixi, cargo, bun",
    ),
    "packages": (packages_section, "global packages of pixi, uv, cargo, and bun"),
    "disk": (disk_section, "volume sizes, Windows file systems, and Developer Mode"),
}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sections = "\n".join(f"  {name:<13}{help}" for name, (_, help) in SECTIONS.items())
    parser = argparse.ArgumentParser(
        prog="sysinfo.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"sections:\n{sections}\n\n"
            "examples:\n"
            "  uv run sysinfo.py environment\n"
            "  uv run sysinfo.py machine\n"
            "  uv run sysinfo.py paths packages"
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
        print(
            json.dumps(
                dict(zip(names, results, strict=True)), ensure_ascii=False, indent=2
            )
        )


if __name__ == "__main__":
    main()
