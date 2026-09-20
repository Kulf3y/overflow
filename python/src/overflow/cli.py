import argparse
import json

from overflow import __version__
from overflow.privacy import redact_text
from overflow.policy import load_policy, validate_policy
from overflow.security import scan_text as security_scan_text
from overflow.audit import AuditChain, default_audit_path, verify_audit_file
from overflow.gateway import serve as serve_gateway
from overflow.optimizer import optimize_text
from overflow.pipeline import process_text


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


def handle_optimize(args):
    report = optimize_text(args.text)

    print("output:", report.output)
    print("original_tokens:", report.original_tokens)
    print("optimized_tokens:", report.optimized_tokens)
    print("reduction_percent:", report.reduction_percent)


def handle_chat(args):
    result = process_text(
        args.text,
        provider_name=args.provider,
        optimize=not args.no_optimize,
        audit_enabled=True
    )

    print("allowed:", result.allowed)

    if not result.allowed:
        print("reasons:", json.dumps(result.reasons, indent=2, sort_keys=True))
        raise SystemExit(1)

    print("output_text:", result.output_text)
    print("response_text:", result.response_text)
    print("privacy_counts:", json.dumps(result.privacy_counts, indent=2, sort_keys=True))
    print("security_counts:", json.dumps(result.security_counts, indent=2, sort_keys=True))
    print("optimization:", json.dumps(result.optimization, indent=2, sort_keys=True))
    print("provider:", result.provider)


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


def handle_gateway(args):
    if args.host != "127.0.0.1" and args.host != "localhost":
        print("Warning: binding to a non-local host can expose the gateway.")

    serve_gateway(host=args.host, port=args.port)


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

    optimize_parser = subparsers.add_parser(
        "optimize",
        help="Optimize text"
    )
    optimize_parser.add_argument("text")

    chat_parser = subparsers.add_parser(
        "chat",
        help="Run the full Overflow pipeline"
    )
    chat_parser.add_argument("text")
    chat_parser.add_argument("--provider", default="mock")
    chat_parser.add_argument("--no-optimize", action="store_true")

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

    gateway_parser = subparsers.add_parser(
        "gateway",
        help="Run the local Overflow gateway"
    )
    gateway_parser.add_argument("--host", default="127.0.0.1")
    gateway_parser.add_argument("--port", type=int, default=8080)

    args = parser.parse_args()

    if args.command == "check":
        handle_check(args)
    elif args.command == "security":
        handle_security(args)
    elif args.command == "optimize":
        handle_optimize(args)
    elif args.command == "chat":
        handle_chat(args)
    elif args.command == "audit":
        handle_audit(args, audit_parser)
    elif args.command == "policy":
        handle_policy(args, policy_parser)
    elif args.command == "gateway":
        handle_gateway(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
