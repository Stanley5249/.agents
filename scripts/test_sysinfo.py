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


if __name__ == "__main__":
    unittest.main()
