# Policies

This folder contains Overflow policy files.

Overflow currently uses JSON policies because Python can read JSON without extra dependencies.

YAML support is planned for a later phase.

## Current policies

- `eu_default.json`
- `eu_strict.json`

## Validate policies

If Python is installed, run:

```powershell
powershell -File scripts\check_policy.ps1
```
