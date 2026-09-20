import unittest

from overflow.native import native_available, native_redact_emails


class NativeTests(unittest.TestCase):
    def test_redact_works(self):
        out, count = native_redact_emails("mail jane@example.com")
        self.assertEqual(count, 1)
        self.assertIn("[EMAIL_REDACTED]", out)

    def test_available_flag_is_bool(self):
        self.assertIsInstance(native_available(), bool)


if __name__ == "__main__":
    unittest.main()
