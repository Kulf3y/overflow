import pathlib
import tempfile
import unittest

from overflow.cache import SemanticCache


class CacheTests(unittest.TestCase):
    def test_put_and_get_similar(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = SemanticCache(path=pathlib.Path(tmp) / "c.db", threshold=0.8)
            cache.put("What is the EU AI Act?", "The EU AI Act is a regulation.", "mock")
            hit = cache.get("What is the EU AI Act?", provider="mock")
            self.assertIsNotNone(hit)
            self.assertEqual(hit["response"], "The EU AI Act is a regulation.")

    def test_provider_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = SemanticCache(path=pathlib.Path(tmp) / "c.db", threshold=0.8)
            cache.put("What is the EU AI Act?", "answer", "mock")
            hit = cache.get("What is the EU AI Act?", provider="openai_compatible")
            self.assertIsNone(hit)

    def test_no_match_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = SemanticCache(path=pathlib.Path(tmp) / "c.db", threshold=0.8)
            cache.put("alpha beta gamma delta", "response one", "mock")
            hit = cache.get("completely different topic about cooking recipes", provider="mock")
            self.assertIsNone(hit)


if __name__ == "__main__":
    unittest.main()
