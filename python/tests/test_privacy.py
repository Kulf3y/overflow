import unittest

from overflow.privacy import redact_text


class PrivacyTests(unittest.TestCase):
    def test_redacts_email(self):
        report = redact_text("Contact jane@example.com")
        self.assertEqual(report.counts.get("EMAIL", 0), 1)
        self.assertEqual(report.emails_found, 1)
        self.assertIn("[EMAIL_REDACTED]", report.output)
        self.assertNotIn("jane@example.com", report.output)

    def test_redacts_phone(self):
        report = redact_text("Call me at +49 30 12345678")
        self.assertEqual(report.counts.get("PHONE", 0), 1)
        self.assertIn("[PHONE_REDACTED]", report.output)
        self.assertNotIn("+49 30 12345678", report.output)

    def test_redacts_iban(self):
        report = redact_text("My IBAN is DE89370400440532013000")
        self.assertEqual(report.counts.get("IBAN", 0), 1)
        self.assertIn("[IBAN_REDACTED]", report.output)
        self.assertNotIn("DE89370400440532013000", report.output)

    def test_custom_pattern(self):
        custom_patterns = [
            {
                "name": "employee_id",
                "pattern": "EMP-[0-9]{6}"
            }
        ]

        report = redact_text("Employee ID EMP-123456", custom_patterns)
        self.assertEqual(report.counts.get("EMPLOYEE_ID", 0), 1)
        self.assertIn("[CUSTOM_EMPLOYEE_ID_REDACTED]", report.output)
        self.assertNotIn("EMP-123456", report.output)

    def test_no_sensitive_data(self):
        report = redact_text("This is normal text.")
        self.assertEqual(report.counts, {})
        self.assertEqual(report.output, "This is normal text.")


if __name__ == "__main__":
    unittest.main()
