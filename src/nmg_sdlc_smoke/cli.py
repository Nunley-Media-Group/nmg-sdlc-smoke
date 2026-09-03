import argparse
import importlib.metadata

from .greet import greet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nmg-smoke")
    parser.add_argument(
        "--version",
        action="version",
        version=importlib.metadata.version("nmg-sdlc-smoke-python"),
    )
    parser.add_argument("name")
    args = parser.parse_args(argv)

    try:
        message = greet(args.name)
    except ValueError as error:
        parser.exit(1, f"nmg-smoke: error: {error}\n")

    print(message)
    return 0
