"""Test process facts without depending on the host platform."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import sysinfo


class EnvironmentTests(unittest.TestCase):
    def test_native_platforms(self):
        for system, release, machine in (
            ("Windows", "11", "AMD64"),
            ("Linux", "6.8.0", "x86_64"),
            ("Darwin", "24.0.0", "arm64"),
        ):
            with (
                self.subTest(system=system),
                patch.dict(os.environ, {}, clear=True),
                patch.object(sysinfo.platform, "system", return_value=system),
                patch.object(sysinfo.platform, "release", return_value=release),
                patch.object(sysinfo.platform, "machine", return_value=machine),
                patch.object(
                    sysinfo.Path, "home", return_value=Path("home with spaces")
                ),
            ):
                self.assertEqual(
                    sysinfo.environment_section(),
                    {
                        "system": system,
                        "release": release,
                        "machine": machine,
                        "home": str(Path("home with spaces")),
                    },
                )

    def test_wsl_variable_is_reported_without_conversion(self):
        with patch.dict(os.environ, {"WSL_DISTRO_NAME": "Custom Distro"}):
            self.assertEqual(
                sysinfo.environment_section()["WSL_DISTRO_NAME"], "Custom Distro"
            )

    def test_cli_uses_utf8_even_when_default_encoding_is_ascii(self):
        env = os.environ | {
            "PYTHONIOENCODING": "ascii",
            "WSL_DISTRO_NAME": "測試 Distro",
        }
        result = subprocess.run(
            [sys.executable, str(Path(sysinfo.__file__)), "environment"],
            capture_output=True,
            check=True,
            env=env,
            timeout=10,
        )
        self.assertEqual(result.stderr, b"")
        self.assertEqual(
            json.loads(result.stdout.decode("utf-8"))["environment"]["WSL_DISTRO_NAME"],
            "測試 Distro",
        )

    def test_no_arguments_still_show_help(self):
        result = subprocess.run(
            [sys.executable, str(Path(sysinfo.__file__))],
            capture_output=True,
            check=True,
            timeout=10,
        )
        self.assertIn(b"usage:", result.stdout)
        self.assertIn(b"environment", result.stdout)


class CommandTests(unittest.TestCase):
    def test_run_returns_none_on_command_failure(self):
        result = subprocess.CompletedProcess(["tool"], 1, b"partial output", b"error")
        with patch.object(sysinfo.subprocess, "run", return_value=result):
            self.assertIsNone(sysinfo.run("tool"))

    def test_run_returns_none_on_timeout_or_missing_command(self):
        for error in (subprocess.TimeoutExpired("tool", 30), FileNotFoundError()):
            with (
                self.subTest(error=type(error).__name__),
                patch.object(sysinfo.subprocess, "run", side_effect=error),
            ):
                self.assertIsNone(sysinfo.run("tool"))


class PackageTests(unittest.TestCase):
    def test_output_lines_preserves_indentation_and_blank_lines(self):
        with patch.object(sysinfo, "run", return_value="package\n  executable\n\nnext"):
            self.assertEqual(
                sysinfo.output_lines("tool", "list"),
                ["package", "  executable", "", "next"],
            )

    def test_packages_distinguish_empty_output_from_failure(self):
        with patch.object(sysinfo, "run", side_effect=["", None, "cargo", "bun"]):
            self.assertEqual(
                sysinfo.packages_section(),
                {"pixi": [], "uv": None, "cargo": ["cargo"], "bun": ["bun"]},
            )


class PixiTests(unittest.TestCase):
    def test_invalid_json_returns_none(self):
        for output in ("not json", ""):
            with (
                self.subTest(output=output),
                patch.object(sysinfo, "run", return_value=output),
            ):
                self.assertIsNone(sysinfo.pixi_paths())

    def test_command_failure_returns_none(self):
        with patch.object(sysinfo, "run", return_value=None):
            self.assertIsNone(sysinfo.pixi_paths())

    def test_valid_json_extracts_paths(self):
        output = json.dumps(
            {
                "global_info": {"bin_dir": "bin", "env_dir": "envs"},
                "cache_dir": "cache",
            }
        )
        with patch.object(sysinfo, "run", return_value=output):
            self.assertEqual(
                sysinfo.pixi_paths(), {"bin": "bin", "envs": "envs", "cache": "cache"}
            )


class WslTests(unittest.TestCase):
    def test_windows_distro_lines_are_trimmed(self):
        with (
            patch.object(sysinfo, "PLATFORM", sysinfo.WINDOWS),
            patch.object(
                sysinfo, "run", return_value=" Ubuntu\r\n\r\n Custom Distro \r\n"
            ) as run,
        ):
            self.assertEqual(sysinfo.wsl_distros(), ["Ubuntu", "Custom Distro"])
            run.assert_called_once_with(
                "wsl", "--list", "--quiet", encoding="utf-16-le"
            )

    def test_windows_distinguishes_no_distros_from_command_failure(self):
        for output, expected in (("", []), (None, None)):
            with (
                self.subTest(output=output),
                patch.object(sysinfo, "PLATFORM", sysinfo.WINDOWS),
                patch.object(sysinfo, "run", return_value=output),
            ):
                self.assertEqual(sysinfo.wsl_distros(), expected)

    def test_non_windows_skips_command(self):
        for platform in (sysinfo.WSL, "linux"):
            with (
                self.subTest(platform=platform),
                patch.object(sysinfo, "PLATFORM", platform),
                patch.object(sysinfo, "run") as run,
            ):
                self.assertIsNone(sysinfo.wsl_distros())
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
