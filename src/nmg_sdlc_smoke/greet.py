import base64
import codecs
import hashlib
import string
import zlib
from collections.abc import Iterable
from urllib.parse import quote


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


def greeting_reversed(name: str) -> str:
    return greet(name)[::-1]


def greeting_word_count(name: str) -> int:
    return len(greet(name).split())


def greeting_vowel_count(name: str) -> int:
    return sum(character in "aeiouAEIOU" for character in greet(name))


def greeting_uppercase_count(name: str) -> int:
    return sum("A" <= character <= "Z" for character in greet(name))


def greeting_lowercase_count(name: str) -> int:
    return sum("a" <= character <= "z" for character in greet(name))


def greeting_digit_count(name: str) -> int:
    return sum("0" <= character <= "9" for character in greet(name))


def greeting_space_count(name: str) -> int:
    return greet(name).count(" ")


def greeting_punctuation_count(name: str) -> int:
    return sum(character in string.punctuation for character in greet(name))


def greeting_unique_char_count(name: str) -> int:
    return len(set(greet(name)))


def greeting_letter_count(name: str) -> int:
    return sum(character.isalpha() for character in greet(name))


def greeting_sha256(name: str) -> str:
    return hashlib.sha256(greet(name).encode("utf-8")).hexdigest()


def greeting_md5(name: str) -> str:
    return hashlib.md5(greet(name).encode("utf-8")).hexdigest()


def greeting_sha1(name: str) -> str:
    return hashlib.sha1(greet(name).encode("utf-8")).hexdigest()


def greeting_base64(name: str) -> str:
    return base64.b64encode(greet(name).encode("utf-8")).decode("ascii")


def greeting_rot13(name: str) -> str:
    return codecs.encode(greet(name), "rot13")


def greeting_url_encoded(name: str) -> str:
    return quote(greet(name), safe="")


def greeting_crc32(name: str) -> int:
    return zlib.crc32(greet(name).encode("utf-8"))


def greeting_adler32(name: str) -> int:
    return zlib.adler32(greet(name).encode("utf-8"))


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


def greeting_has_asterisk(name: str) -> bool:
    return "*" in greet(name)


def greeting_has_ascii_asterisk(name: str) -> bool:
    return "*" in greet(name)


def greeting_has_exclamation(name: str) -> bool:
    return "!" in greet(name)


def greeting_has_exclamation_or_question(name: str) -> bool:
    greeting = greet(name)
    return "!" in greeting or "?" in greeting


def greeting_has_dollar(name: str) -> bool:
    return "$" in greet(name)


def greeting_has_double_quote(name: str) -> bool:
    return '"' in greet(name)


def greeting_has_underscore(name: str) -> bool:
    return "_" in greet(name)


def greeting_has_slash(name: str) -> bool:
    return "/" in greet(name)


def greeting_has_backslash(name: str) -> bool:
    return "\\" in greet(name)


def greeting_has_apostrophe(name: str) -> bool:
    return "'" in greet(name)
