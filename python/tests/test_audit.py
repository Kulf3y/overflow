import tempfile
import unittest
from pathlib import Path

from overflow.audit import AuditChain, verify_audit_file


class AuditTests(unittest.TestCase):
    def test_log_and_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.jsonl"
            chain = AuditChain(path)

            chain.log_event("test_event", metadata={"safe": True})
            chain.log_event("another_event")

            report = verify_audit_file(path)

            self.assertTrue(report.valid)
            self.assertEqual(report.entries, 2)

    def test_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.jsonl"
            chain = AuditChain(path)

            chain.log_event("test_event")

            text = path.read_text(encoding="utf-8")
            tampered = text.replace("test_event", "tampered_event")
            path.write_text(tampered, encoding="utf-8")

            report = verify_audit_file(path)

            self.assertFalse(report.valid)

    def test_missing_file_is_empty_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.jsonl"
            report = verify_audit_file(path)

            self.assertTrue(report.valid)
            self.assertEqual(report.entries, 0)


if __name__ == "__main__":
    unittest.main()
