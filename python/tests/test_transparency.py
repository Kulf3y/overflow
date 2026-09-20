import unittest

from overflow.transparency import DEFAULT_NOTICE, apply_watermark


class TransparencyTests(unittest.TestCase):
    def test_appends_notice(self):
        out = apply_watermark("Hello")
        self.assertTrue(out.endswith(DEFAULT_NOTICE))
        self.assertIn("Hello", out)


if __name__ == "__main__":
    unittest.main()
