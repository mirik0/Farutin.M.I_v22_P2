import io
import tarfile
import unittest
from unittest.mock import patch

from src.repository import Repository, load_apk, parse_index

INDEX = """P:tool
V:1.0-r0
D:so:libc.so.1
p:cmd:tool=1.0

P:tool
V:2.0-r0
D:lib

P:lib
V:1.0-r0
"""


class RepositoryTests(unittest.TestCase):

    def test_exact_version(self):
        repo = Repository(parse_index(INDEX))
        self.assertEqual(repo.get("tool", "2.0-r0")["depends"], ["lib"])
        with self.assertRaises(ValueError):
            repo.get("tool", "3.0-r0")

    def test_archive(self):
        data = INDEX.encode()
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
            info = tarfile.TarInfo("APKINDEX")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
        buffer.seek(0)
        with patch("src.repository.urlopen", return_value=buffer) as fetch:
            repo = load_apk("https://example.org/main/x86_64/")
        self.assertEqual(repo.get("tool", "1.0-r0")["depends"],
                         ["so:libc.so.1"])
        self.assertEqual(fetch.call_args.args[0],
                         "https://example.org/main/x86_64/APKINDEX.tar.gz")
