import unittest

from overflow.optimizer import estimate_tokens, optimize_text


class OptimizerTests(unittest.TestCase):
    def test_estimate_tokens_empty(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_estimate_tokens_not_empty(self):
        self.assertGreater(estimate_tokens("hello world"), 0)

    def test_removes_duplicate_lines(self):
        text = "line\nline\nother"
        report = optimize_text(text)

        self.assertIn("other", report.output)
        self.assertEqual(report.output.splitlines().count("line"), 1)

    def test_reduction_not_negative(self):
        report = optimize_text("  hello   world  ")
        self.assertGreaterEqual(report.reduction_percent, 0.0)


if __name__ == "__main__":
    unittest.main()
