import unittest
import time
import tracemalloc
import random
from main import task1_trie, task2_aho

class TestPrefixTrie(unittest.TestCase):
    def test_task1_simple(self):
        patterns = ["CGT"]
        edges = task1_trie(patterns)
        expected = {"0->1:C", "1->2:G", "2->3:T"}
        self.assertEqual(set(edges), expected)

    def test_task1_multiple(self):
        patterns = ["CG", "CC", "CT"]
        edges = task1_trie(patterns)
        self.assertEqual(len(edges), 4)
        self.assertTrue(any(e.startswith("0->") and e.endswith(":C") for e in edges))

    def test_task1_performance(self):
        patterns = ["A" * 100 for _ in range(100)]
        start = time.time()
        _ = task1_trie(patterns)
        duration = time.time() - start
        print(f"[Performance] Task1-Trie speed: {duration:.4f}s")
        self.assertLess(duration, 0.5)

    def test_task1_memory(self):
        patterns = ["A" * 100 for _ in range(100)]
        tracemalloc.start()
        _ = task1_trie(patterns)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / 1024 / 1024
        print(f"[Memory] Task1-Trie peak: {peak_mb:.2f} MB")
        self.assertLess(peak, 50 * 1024 * 1024)

class TestAhoCorasick(unittest.TestCase):
    def test_task2_simple(self):
        text = "ATTCCGATA"
        patterns = ["AT", "C"]
        matches = task2_aho(text, patterns)
        self.assertEqual(matches, [0, 3, 4, 6])

    def test_task2_no_match(self):
        text = "AAAA"
        patterns = ["C", "G"]
        matches = task2_aho(text, patterns)
        self.assertEqual(matches, [])

    def test_task2_performance(self):
        text = "".join(random.choices("ACGT", k=10000))
        patterns = ["".join(random.choices("ACGT", k=100)) for _ in range(1000)]
        start = time.time()
        _ = task2_aho(text, patterns)
        duration = time.time() - start
        print(f"[Performance] Aho-Corasick speed: {duration:.4f}s")
        self.assertLess(duration, 2.0)

    def test_task2_memory(self):
        text = "".join(random.choices("ACGT", k=10000))
        patterns = ["".join(random.choices("ACGT", k=100)) for _ in range(1000)]
        tracemalloc.start()
        _ = task2_aho(text, patterns)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / 1024 / 1024
        print(f"[Memory] Aho-Corasick peak: {peak_mb:.2f} MB")
        self.assertLess(peak, 100 * 1024 * 1024)

if __name__ == "__main__":
    unittest.main(verbosity=2)
