import unittest

from overflow.privacy import redact_emails


class PrivacyTests(unittest.TestCase):
    def test_redacts_email(self):
        report = redact_emails("Contact jane@example.com")
        self.assertEqual(report.emails_found, 1)
        self.assertIn("[EMAIL_REDACTED]", report.output)
        self.assertNotIn("jane@example.com", report.output)

    def test_redacts_multiple_emails(self):
        report = redact_emails("a@example.com and b@example.org")
        self.assertEqual(report.emails_found, 2)

    def test_no_email(self):
        report = redact_emails("No contact here")
        self.assertEqual(report.emails_found, 0)
        self.assertEqual(report.output, "No contact here")


if __name__ == "__main__":
    unittest.main()
