# Overflow Policies

Overflow policies define how requests should be handled.

Current policy format: JSON.

YAML support is planned later.

## Policy sections

### privacy

Controls data minimization behavior.

- `redact_pii`
- `redact_secrets`

### security

Controls security guardrails.

- `block_prompt_injection`
- `block_jailbreak_attempts`

### routing

Controls where requests may be sent.

- `allow_external_providers`
- `fallback`
- `allowed_regions`

### audit

Controls audit behavior.

- `enabled`
- `store_raw_prompts`
- `store_raw_responses`

## Important design rule

Overflow should fail closed when a critical policy cannot be guaranteed.
