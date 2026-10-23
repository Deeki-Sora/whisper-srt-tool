"""Run Windows CMD regression checks without loading or downloading models."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name == "nt", "These launchers require Windows CMD")
class LauncherTests(unittest.TestCase):
    def invoke(self, root, name, args="", stdin="", path=None):
        env = os.environ.copy()
        env["WHISPERSRT_NO_PAUSE"] = "1"
        env["PYTHONUTF8"] = "1"
        if path is not None:
            env["PATH"] = path
        cmd = os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe")
        return subprocess.run(
            f'"{cmd}" /d /s /c ""{root / name}" {args}"',
            input=stdin, text=True, encoding="utf-8", errors="strict",
            capture_output=True, env=env, cwd=tempfile.gettempdir(), timeout=90,
        )

    def test_bat_encoding_and_line_endings(self):
        for path in ROOT.glob("*.bat"):
            data = path.read_bytes()
            data.decode("ascii")
            self.assertNotIn(b"\n", data.replace(b"\r\n", b""), path.name)
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"), path.name)

    def test_help_from_other_working_directory(self):
        result = self.invoke(ROOT, "run_whisper_srt.bat", "--help")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("灏嗘湰鏈洪煶棰?瑙嗛", result.stdout)
        self.assertNotIn("\ufffd", result.stdout)

    def test_interactive_exit(self):
        result = self.invoke(ROOT, "run_whisper_srt.bat", stdin="\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("璺緞锛?, result.stdout)
        self.assertIn("鏈寚瀹氳矾寰?, result.stdout)

    def test_installer_reuses_system_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "宸ュ叿 test & (璺緞)!"
            root.mkdir()
            for path in ROOT.iterdir():
                if path.suffix in {".bat", ".py"}:
                    shutil.copy2(path, root / path.name)
            result = self.invoke(root, "install_whisper_srt.bat")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("No installation needed", result.stdout)
            self.assertFalse((root / ".venv").exists())
            help_result = self.invoke(root, "run_whisper_srt.bat", "--help")
            self.assertEqual(help_result.returncode, 0, help_result.stdout + help_result.stderr)
            self.assertIn("灏嗘湰鏈洪煶棰?瑙嗛", help_result.stdout)

    def test_missing_python_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in ROOT.glob("*.bat"):
                shutil.copy2(path, root / path.name)
            shutil.copy2(ROOT / "check_environment.py", root / "check_environment.py")
            windows = Path(os.environ["SystemRoot"])
            result = self.invoke(root, "install_whisper_srt.bat", path=str(windows / "System32"))
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Python 3.10-3.12 is required", result.stdout)
            self.assertFalse((root / ".venv").exists())


if __name__ == "__main__":
    unittest.main()

