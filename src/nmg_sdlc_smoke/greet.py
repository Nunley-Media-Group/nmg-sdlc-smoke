from collections.abc import Iterable


def greet(name: str) -> str:
    """Return a greeting for a non-blank name."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must not be blank")
    return f"Hello, {name}"

def greet_many(names: Iterable[str]) -> list[str]:
    if isinstance(names, str):
        raise TypeError("names must not be a str")
    return [greet(name) for name in names]

def greeting_length(name: str) -> int:
    return len(greet(name))

def greeting_bytes(name: str) -> int:
    return len(greet(name).encode("utf-8"))

def greeting_is_ascii(name: str) -> bool:
    return greet(name).isascii()
