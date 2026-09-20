import argparse

from overflow import __version__
from overflow.privacy import redact_emails


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
        help="Check text for simple email PII"
    )

    check_parser.add_argument("text")

    args = parser.parse_args()

    if args.command == "check":
        report = redact_emails(args.text)
        print("emails_found:", report.emails_found)
        print("redacted:", report.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
