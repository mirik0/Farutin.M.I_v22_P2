import re
import unittest
from pathlib import Path

from src.graph import dependency_graph
from src.plantuml import to_plantuml
from src.repository import Repository, parse_index

ROOT = Path(__file__).resolve().parents[1]


class ExampleTests(unittest.TestCase):

    def test_native_apk_examples(self):
        text = (ROOT / "fixtures/alpine-sample.APKINDEX").read_text()
        repo = Repository(parse_index(text))
        labels = {item["name"] + "-" + item["version"]: item["name"]
                  for item in repo.packages.values()}
        for name in ("busybox", "zlib", "xz"):
            with self.subTest(name=name):
                package = repo.get(name)
                graph = dependency_graph(repo, name, package["version"])
                dot = (ROOT / "examples" / (name + ".apk.dot")).read_text()
                pairs = re.findall(r'"([^"\n]+)" -> "([^"\n]+)"', dot)
                actual = {(labels[a], labels[b]) for a, b in pairs}
                expected = {(a, b) for a, bs in graph.items() for b in bs}
                self.assertEqual(actual, expected)
                puml = (ROOT / "examples" / (name + ".puml")).read_text()
                self.assertEqual(puml, to_plantuml(graph) + "\n")
