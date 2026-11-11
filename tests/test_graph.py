import unittest
from pathlib import Path

from src.graph import dependency_graph, reverse_graph
from src.repository import load_test

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class GraphTests(unittest.TestCase):

    def test_chain(self):
        repo = load_test(FIXTURES / "chain.json")
        self.assertEqual(dependency_graph(repo, "A", "1.0"),
                         {"A": ["B"], "B": ["C"], "C": []})

    def test_diamond_and_version(self):
        repo = load_test(FIXTURES / "diamond.json")
        graph = dependency_graph(repo, "A", "1.0")
        self.assertEqual(list(graph), ["A", "B", "D", "C"])
        self.assertEqual(graph["C"], ["D"])
        self.assertEqual(dependency_graph(repo, "A", "2.0"),
                         {"A": ["C"], "C": ["D"], "D": []})

    def test_cycles(self):
        repo = load_test(FIXTURES / "cycle.json")
        self.assertEqual(dependency_graph(repo, "A", "1.0"),
                         {"A": ["B"], "B": ["C"], "C": ["A"]})
        self.assertEqual(dependency_graph(repo, "D", "1.0"), {"D": ["D"]})
        self.assertEqual(dependency_graph(repo, "E", "1.0"), {"E": []})


    def test_reverse(self):
        cases = [
            ("chain.json", "C", {"C", "B", "A"}),
            ("diamond.json", "D", {"D", "B", "A", "C"}),
            ("cycle.json", "A", {"A", "C", "B"}),
        ]
        for file, name, expected in cases:
            with self.subTest(file=file):
                repo = load_test(FIXTURES / file)
                self.assertEqual(set(reverse_graph(repo, name, "1.0")),
                                 expected)
