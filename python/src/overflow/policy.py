import json
from pathlib import Path

REQUIRED_SECTIONS = ["privacy", "security", "routing", "audit"]

BOOLEAN_PRIVACY_KEYS = ["redact_pii", "redact_secrets"]
BOOLEAN_SECURITY_KEYS = ["block_prompt_injection", "block_jailbreak_attempts"]
BOOLEAN_ROUTING_KEYS = ["allow_external_providers"]
BOOLEAN_AUDIT_KEYS = ["enabled", "store_raw_prompts", "store_raw_responses"]


def load_policy(path):
    policy_path = Path(path)

    if policy_path.suffix.lower() in [".yaml", ".yml"]:
        raise ValueError("YAML policies are planned but not supported yet. Use JSON for now.")

    with open(policy_path, encoding="utf-8") as handle:
        return json.load(handle)


def validate_policy(policy):
    errors = []

    if not isinstance(policy, dict):
        return ["Policy must be a JSON object."]

    for section in REQUIRED_SECTIONS:
        if section not in policy:
            errors.append(f"Missing section: {section}")
            continue

        if not isinstance(policy[section], dict):
            errors.append(f"Section must be an object: {section}")

    privacy = policy.get("privacy")

    if isinstance(privacy, dict):
        for key in BOOLEAN_PRIVACY_KEYS:
            if key in privacy and not isinstance(privacy[key], bool):
                errors.append(f"privacy.{key} must be a boolean")

    security = policy.get("security")

    if isinstance(security, dict):
        for key in BOOLEAN_SECURITY_KEYS:
            if key in security and not isinstance(security[key], bool):
                errors.append(f"security.{key} must be a boolean")

    routing = policy.get("routing")

    if isinstance(routing, dict):
        for key in BOOLEAN_ROUTING_KEYS:
            if key in routing and not isinstance(routing[key], bool):
                errors.append(f"routing.{key} must be a boolean")

        fallback = routing.get("fallback")

        if fallback is not None and fallback not in ["allow", "deny"]:
            errors.append("routing.fallback must be either allow or deny")

        allowed_regions = routing.get("allowed_regions")

        if allowed_regions is not None:
            if not isinstance(allowed_regions, list):
                errors.append("routing.allowed_regions must be a list")
            elif not all(isinstance(region, str) for region in allowed_regions):
                errors.append("routing.allowed_regions must contain only strings")

    audit = policy.get("audit")

    if isinstance(audit, dict):
        for key in BOOLEAN_AUDIT_KEYS:
            if key in audit and not isinstance(audit[key], bool):
                errors.append(f"audit.{key} must be a boolean")

    return errors
