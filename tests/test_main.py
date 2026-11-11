import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.main import main
from src.repository import Repository, parse_index

ROOT = Path(__file__).resolve().parents[1]


class MainTests(unittest.TestCase):

    def launch(self, *extra):
        return subprocess.run(
            [sys.executable, "-m", "src.main", "--package", "zlib",
             "--version", "1.0", "--repo", "https://example.org/main",
             *extra], cwd=ROOT, text=True, capture_output=True,
        )

    def test_bad_options(self):
        cases = [
            ("--package", "bad name"), ("--version", ""),
            ("--repo", "wrong"), ("--repo", "https://["),
            ("--test-repo=yes",),
            ("--package", "A", "--test-repo", "--repo", "missing.json"),
        ]
        for args in cases:
            with self.subTest(args=args):
                result = self.launch(*args)
                self.assertEqual(result.returncode, 2)

    def test_result(self):
        repo = Repository(parse_index("P:tool\nV:1.0\nD:lib\n"))
        output = io.StringIO()
        with patch("src.main.load_apk", return_value=repo):
            with redirect_stdout(output):
                status = main(["--package", "tool", "--version", "1.0",
                               "--repo", "https://example.org/main"])
        self.assertEqual(status, 0)
        self.assertEqual(output.getvalue(), "lib\n")
