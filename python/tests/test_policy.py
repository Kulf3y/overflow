import json
import tempfile
import unittest
from pathlib import Path

from overflow.policy import load_policy, validate_policy


def make_valid_policy():
    return {
        "privacy": {
            "redact_pii": True,
            "redact_secrets": True
        },
        "security": {
            "block_prompt_injection": True,
            "block_jailbreak_attempts": True
        },
        "routing": {
            "allow_external_providers": False,
            "fallback": "deny",
            "allowed_regions": ["EU"]
        },
        "audit": {
            "enabled": True,
            "store_raw_prompts": False,
            "store_raw_responses": False
        }
    }


class PolicyTests(unittest.TestCase):
    def test_valid_policy(self):
        policy = make_valid_policy()
        errors = validate_policy(policy)
        self.assertEqual(errors, [])

    def test_missing_section(self):
        policy = make_valid_policy()
        del policy["audit"]
        errors = validate_policy(policy)
        self.assertIn("Missing section: audit", errors)

    def test_invalid_boolean(self):
        policy = make_valid_policy()
        policy["privacy"]["redact_pii"] = "yes"
        errors = validate_policy(policy)
        self.assertIn("privacy.redact_pii must be a boolean", errors)

    def test_invalid_fallback(self):
        policy = make_valid_policy()
        policy["routing"]["fallback"] = "maybe"
        errors = validate_policy(policy)
        self.assertIn("routing.fallback must be either allow or deny", errors)

    def test_load_policy_json(self):
        policy = make_valid_policy()

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.json"
            path.write_text(json.dumps(policy), encoding="utf-8")
            loaded = load_policy(str(path))
            self.assertEqual(loaded, policy)


if __name__ == "__main__":
    unittest.main()
