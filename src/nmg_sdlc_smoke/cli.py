import argparse

from .greet import greet


def _positive_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "COUNT must be a positive integer"
        ) from error
    if count < 1:
        raise argparse.ArgumentTypeError("COUNT must be a positive integer")
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nmg-smoke")
    parser.add_argument("--uppercase", action="store_true")
    parser.add_argument(
        "--repeat", type=_positive_count, default=1, metavar="COUNT"
    )
    parser.add_argument("name")
    args = parser.parse_args(argv)

    try:
        message = greet(args.name)
    except ValueError as error:
        parser.exit(1, f"nmg-smoke: error: {error}\n")

    if args.uppercase:
        message = message.upper()
    for _ in range(args.repeat):
        print(message)
    return 0
