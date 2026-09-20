import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

GENESIS_HASH = "0" * 64


def default_audit_path():
    return Path.cwd() / ".overflow" / "audit" / "audit.jsonl"


@dataclass
class VerifyReport:
    valid: bool
    entries: int = 0
    errors: list[str] = field(default_factory=list)


def _canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _hash_entry(entry):
    canonical = _canonical_json(entry)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class AuditChain:
    def __init__(self, path=None):
        if path is None:
            path = default_audit_path()

        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _last_hash(self):
        if not self.path.exists():
            return GENESIS_HASH

        last_line = None

        with open(self.path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()

                if line:
                    last_line = line

        if not last_line:
            return GENESIS_HASH

        entry = json.loads(last_line)
        return entry.get("current_hash", GENESIS_HASH)

    def log_event(self, event_type, metadata=None, trace_id=None):
        previous_hash = self._last_hash()

        if trace_id is None:
            trace_id = str(uuid.uuid4())

        if metadata is None:
            metadata = {}

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
            "event_type": event_type,
            "metadata": metadata,
            "previous_hash": previous_hash
        }

        current_hash = _hash_entry(entry)
        entry["current_hash"] = current_hash

        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")

        return entry


def verify_audit_file(path=None):
    if path is None:
        path = default_audit_path()

    audit_path = Path(path)
    errors = []
    entries = 0

    if not audit_path.exists():
        return VerifyReport(valid=True, entries=0, errors=errors)

    previous_hash = GENESIS_HASH

    with open(audit_path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()

            if not line:
                continue

            entries += 1

            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                errors.append(f"line {line_number}: invalid JSON")
                return VerifyReport(valid=False, entries=entries, errors=errors)

            stored_hash = entry.get("current_hash")

            if not stored_hash:
                errors.append(f"line {line_number}: missing current_hash")
                return VerifyReport(valid=False, entries=entries, errors=errors)

            if entry.get("previous_hash") != previous_hash:
                errors.append(f"line {line_number}: broken chain")
                return VerifyReport(valid=False, entries=entries, errors=errors)

            entry_without_hash = dict(entry)
            del entry_without_hash["current_hash"]

            computed_hash = _hash_entry(entry_without_hash)

            if computed_hash != stored_hash:
                errors.append(f"line {line_number}: hash mismatch")
                return VerifyReport(valid=False, entries=entries, errors=errors)

            previous_hash = stored_hash

    return VerifyReport(valid=len(errors) == 0, entries=entries, errors=errors)
