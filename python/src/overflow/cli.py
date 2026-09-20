import argparse
import json

from overflow import __version__
from overflow.privacy import redact_text
from overflow.policy import load_policy, validate_policy
from overflow.security import scan_text as security_scan_text
from overflow.audit import AuditChain, default_audit_path, verify_audit_file


def handle_check(args):
    report = redact_text(args.text)
    print("redacted:", report.output)
    print("counts:", json.dumps(report.counts, indent=2, sort_keys=True))


def handle_security(args):
    report = security_scan_text(args.text)

    print("allowed:", report.allowed)
    print("reasons:", json.dumps(report.reasons, indent=2, sort_keys=True))
    print("counts:", json.dumps(report.counts, indent=2, sort_keys=True))

    if not report.allowed:
        raise SystemExit(1)


def handle_audit(args, parser):
    if args.audit_command == "log":
        path = args.file if args.file else None
        chain = AuditChain(path)

        metadata = {}

        if args.note:
            metadata["note"] = args.note

        entry = chain.log_event(args.event_type, metadata=metadata)

        print("trace_id:", entry["trace_id"])
        print("current_hash:", entry["current_hash"])
    elif args.audit_command == "verify":
        path = args.file if args.file else None
        report = verify_audit_file(path)

        print("valid:", report.valid)
        print("entries:", report.entries)

        if report.errors:
            print("errors:")

            for error in report.errors:
                print("-", error)

            raise SystemExit(1)
    elif args.audit_command == "path":
        print(default_audit_path())
    else:
        parser.print_help()


def handle_policy(args, parser):
    if args.policy_command == "validate":
        policy = load_policy(args.path)
        errors = validate_policy(policy)

        if errors:
            print("Policy validation failed:")

            for error in errors:
                print("-", error)

            raise SystemExit(1)

        print("Policy is valid.")
    elif args.policy_command == "show":
        policy = load_policy(args.path)
        print(json.dumps(policy, indent=2, sort_keys=True))
    else:
        parser.print_help()


def main():
    parser = argparse.ArgumentParser(
        prog="overflow",
        description="Overflow CLI"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=__version__
    )

    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser(
        "check",
        help="Check text for privacy-sensitive data"
    )
    check_parser.add_argument("text")

    security_parser = subparsers.add_parser(
        "security",
        help="Check text for security risks"
    )
    security_parser.add_argument("text")

    audit_parser = subparsers.add_parser(
        "audit",
        help="Audit commands"
    )
    audit_subparsers = audit_parser.add_subparsers(dest="audit_command")

    log_parser = audit_subparsers.add_parser(
        "log",
        help="Log an audit event"
    )
    log_parser.add_argument("event_type")
    log_parser.add_argument("--note")
    log_parser.add_argument("--file")

    verify_parser = audit_subparsers.add_parser(
        "verify",
        help="Verify audit chain"
    )
    verify_parser.add_argument("--file")

    path_parser = audit_subparsers.add_parser(
        "path",
        help="Show default audit path"
    )

    policy_parser = subparsers.add_parser(
        "policy",
        help="Policy commands"
    )
    policy_subparsers = policy_parser.add_subparsers(dest="policy_command")

    validate_parser = policy_subparsers.add_parser(
        "validate",
        help="Validate a policy file"
    )
    validate_parser.add_argument("path")

    show_parser = policy_subparsers.add_parser(
        "show",
        help="Show a policy file"
    )
    show_parser.add_argument("path")

    args = parser.parse_args()

    if args.command == "check":
        handle_check(args)
    elif args.command == "security":
        handle_security(args)
    elif args.command == "audit":
        handle_audit(args, audit_parser)
    elif args.command == "policy":
        handle_policy(args, policy_parser)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
