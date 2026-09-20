import argparse
import json

from overflow import __version__
from overflow.privacy import redact_text
from overflow.policy import load_policy, validate_policy
from overflow.security import scan_text as security_scan_text


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
    elif args.command == "policy":
        handle_policy(args, policy_parser)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
