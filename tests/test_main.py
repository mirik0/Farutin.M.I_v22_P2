import subprocess
import sys
import unittest
from pathlib import Path

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
        result = self.launch("--test-repo",
                             "--repo", "fixtures/chain.json",
                             "--package", "C")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("B\nA\n"))
