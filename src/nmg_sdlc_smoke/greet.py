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


def greeting_starts_with_hello(name: str) -> bool:
    return greet(name).startswith("Hello, ")


def greeting_ends_with_name(name: str) -> bool:
    return greet(name).endswith(name)


def greeting_ends_with_exclamation(name: str) -> str:
    return f"{greet(name)}!"


def greeting_casefold(name: str) -> str:
    return greet(name).casefold()


def greeting_word_count(name: str) -> int:
    return len(greet(name).split())


def greeting_has_semicolon(name: str) -> bool:
    return ";" in greet(name)


def greeting_has_colon(name: str) -> bool:
    return ":" in greet(name)


def greeting_has_at_sign(name: str) -> bool:
    return "@" in greet(name)


def greeting_has_question_mark(name: str) -> bool:
    return "?" in greet(name)


def greeting_has_percent(name: str) -> bool:
    return "%" in greet(name)


def greeting_has_hash(name: str) -> bool:
    return "#" in greet(name)


def greeting_has_plus(name: str) -> bool:
    return "+" in greet(name)


def greeting_has_equal(name: str) -> bool:
    return "=" in greet(name)


def greeting_has_backtick(name: str) -> bool:
    return "\u0060" in greet(name)
