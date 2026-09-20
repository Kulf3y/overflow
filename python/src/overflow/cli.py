import argparse
import json

from overflow import __version__
from overflow.privacy import redact_text
from overflow.policy import load_policy, validate_policy
from overflow.security import scan_text as security_scan_text
from overflow.audit import AuditChain, default_audit_path, verify_audit_file
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
    print("response_text:", result.response_text)
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
    try:
        import uvicorn
        from overflow.gateway import app
    except ImportError as exc:
        print(f"Gateway requires dependencies: {exc}")
        print("Install with: pip install -e python")
        raise SystemExit(1)

    if args.host != "127.0.0.1" and args.host != "localhost":
        print("Warning: binding to a non-local host.")

    print(f"Starting Overflow gateway on http://{args.host}:{args.port}")
    print(f"API docs: http://{args.host}:{args.port}/docs")
    print(f"Dashboard: http://{args.host}:{args.port}/dashboard")
    uvicorn.run(app, host=args.host, port=args.port)


def main():
    parser = argparse.ArgumentParser(
        prog="overflow",
        description="Overflow CLI"
    )
    parser.add_argument(
        "--version", action="version", version=__version__
    )

    subparsers = parser.add_subparsers(dest="command")

    check_p = subparsers.add_parser("check", help="Check text for PII")
    check_p.add_argument("text")

    sec_p = subparsers.add_parser("security", help="Security scan")
    sec_p.add_argument("text")

    opt_p = subparsers.add_parser("optimize", help="Optimize text")
    opt_p.add_argument("text")

    chat_p = subparsers.add_parser("chat", help="Run pipeline")
    chat_p.add_argument("text")
    chat_p.add_argument("--provider", default="mock")
    chat_p.add_argument("--no-optimize", action="store_true")

    audit_p = subparsers.add_parser("audit", help="Audit commands")
    audit_sub = audit_p.add_subparsers(dest="audit_command")
    log_p = audit_sub.add_parser("log")
    log_p.add_argument("event_type")
    log_p.add_argument("--note")
    log_p.add_argument("--file")
    ver_p = audit_sub.add_parser("verify")
    ver_p.add_argument("--file")
    audit_sub.add_parser("path")

    pol_p = subparsers.add_parser("policy", help="Policy commands")
    pol_sub = pol_p.add_subparsers(dest="policy_command")
    val_p = pol_sub.add_parser("validate")
    val_p.add_argument("path")
    show_p = pol_sub.add_parser("show")
    show_p.add_argument("path")

    gw_p = subparsers.add_parser("gateway", help="Run gateway")
    gw_p.add_argument("--host", default="127.0.0.1")
    gw_p.add_argument("--port", type=int, default=8080)

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
        handle_audit(args, audit_p)
    elif args.command == "policy":
        handle_policy(args, pol_p)
    elif args.command == "gateway":
        handle_gateway(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
