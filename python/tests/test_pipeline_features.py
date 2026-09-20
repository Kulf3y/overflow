import unittest
import uuid

from overflow.pipeline import process_text


class PipelineFeatureTests(unittest.TestCase):
    def test_watermark_applied(self):
        question = f"watermark question {uuid.uuid4()}"
        result = process_text(question, audit_enabled=False)
        self.assertTrue(result.watermarked)

    def test_cache_hit_on_repeat(self):
        question = f"unique caching question {uuid.uuid4()}"
        first = process_text(question, audit_enabled=False)
        second = process_text(question, audit_enabled=False)
        self.assertFalse(first.cached)
        self.assertTrue(second.cached)
        self.assertEqual(second.provider, "cache")


if __name__ == "__main__":
    unittest.main()
