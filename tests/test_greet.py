import codecs
import hashlib
import zlib
from urllib.parse import unquote

import pytest

from nmg_sdlc_smoke import (
    greet,
    greet_many,
    greeting_adler32,
    greeting_base64,
    greeting_bytes,
    greeting_casefold,
    greeting_crc32,
    greeting_digit_count,
    greeting_ends_with_exclamation,
    greeting_ends_with_name,
    greeting_has_apostrophe,
    greeting_has_ascii_asterisk,
    greeting_has_asterisk,
    greeting_has_at_sign,
    greeting_has_backslash,
    greeting_has_backtick,
    greeting_has_colon,
    greeting_has_dollar,
    greeting_has_double_quote,
    greeting_has_equal,
    greeting_has_exclamation,
    greeting_has_exclamation_or_question,
    greeting_has_hash,
    greeting_has_percent,
    greeting_has_plus,
    greeting_has_question_mark,
    greeting_has_semicolon,
    greeting_has_slash,
    greeting_has_underscore,
    greeting_is_ascii,
    greeting_length,
    greeting_letter_count,
    greeting_lowercase_count,
    greeting_md5,
    greeting_punctuation_count,
    greeting_reversed,
    greeting_rot13,
    greeting_sha1,
    greeting_sha256,
    greeting_sha512,
    greeting_space_count,
    greeting_starts_with_hello,
    greeting_unique_char_count,
    greeting_uppercase_count,
    greeting_url_encoded,
    greeting_vowel_count,
    greeting_word_count,
)


def test_greet_returns_exact_message() -> None:
    assert greet("Ada") == "Hello, Ada"


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greet_rejects_blank_and_non_string_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet(name)  # type: ignore[arg-type]

def test_greet_many_returns_greetings_in_order_with_duplicates() -> None:
    assert greet_many(["Ada", "Bob"]) == ["Hello, Ada", "Hello, Bob"]
    assert greet_many(["Ada", "Ada"]) == ["Hello, Ada", "Hello, Ada"]


def test_greet_many_returns_empty_list_for_empty_iterables() -> None:
    assert greet_many([]) == []
    assert greet_many(()) == []
    assert greet_many(name for name in []) == []


def test_greet_many_accepts_tuple_and_generator() -> None:
    expected = ["Hello, Ada", "Hello, Bob"]

    assert greet_many(("Ada", "Bob")) == expected
    assert greet_many(name for name in ["Ada", "Bob"]) == expected


@pytest.mark.parametrize("names", [["Ada", " ", "Bob"], ["", "Bob"], [42, "Bob"]])
def test_greet_many_propagates_first_invalid_name(names: list[object]) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet_many(names)  # type: ignore[arg-type]


def test_greet_many_rejects_bare_string() -> None:
    with pytest.raises(TypeError, match="^names must not be a str$"):
        greet_many("Ada")


def test_greeting_length_returns_full_greeting_length() -> None:
    ada_length = greeting_length("Ada")
    jo_length = greeting_length("Jo")

    assert ada_length == 10
    assert ada_length == len(greet("Ada"))
    assert jo_length == 9
    assert jo_length == len(greet("Jo"))
    assert jo_length != ada_length


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greeting_length_rejects_blank_and_non_string_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_length(name)  # type: ignore[arg-type]


def test_greeting_bytes_returns_ascii_greeting_byte_count() -> None:
    result = greeting_bytes("Ada")

    assert result == 10
    assert result == len(greet("Ada").encode("utf-8"))


def test_greeting_bytes_returns_non_ascii_greeting_byte_count() -> None:
    result = greeting_bytes("É")

    assert result == 9
    assert result == len(greet("É").encode("utf-8"))
    assert greeting_length("É") == 8
    assert result != greeting_length("É")
    assert result != greeting_bytes("Ada")


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greeting_bytes_rejects_blank_and_non_string_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_bytes(name)  # type: ignore[arg-type]


def test_greeting_is_ascii_returns_true_for_ascii_greeting() -> None:
    assert greeting_is_ascii("Ada") is True
    assert greeting_is_ascii("Ada") == greet("Ada").isascii()


def test_greeting_is_ascii_returns_false_for_non_ascii_greeting() -> None:
    assert greeting_is_ascii("É") is False
    assert greeting_is_ascii("É") == greet("É").isascii()
    assert greeting_is_ascii("É") != greeting_is_ascii("Ada")


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greeting_is_ascii_rejects_blank_and_non_string_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_is_ascii(name)  # type: ignore[arg-type]


def test_greeting_starts_with_hello_returns_true_for_ada() -> None:
    result = greeting_starts_with_hello("Ada")

    assert result is True
    assert result == greet("Ada").startswith("Hello, ")


def test_greeting_starts_with_hello_returns_true_for_jo() -> None:
    result = greeting_starts_with_hello("Jo")

    assert result is True
    assert result == greet("Jo").startswith("Hello, ")
    assert greet("Jo") != greet("Ada")


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greeting_starts_with_hello_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_starts_with_hello(name)  # type: ignore[arg-type]


def test_greeting_ends_with_name_returns_true_for_ada() -> None:
    result = greeting_ends_with_name("Ada")

    assert result is True
    assert result == greet("Ada").endswith("Ada")


def test_greeting_ends_with_name_returns_true_for_jo() -> None:
    result = greeting_ends_with_name("Jo")

    assert result is True
    assert result == greet("Jo").endswith("Jo")
    assert greet("Jo") != greet("Ada")


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greeting_ends_with_name_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_ends_with_name(name)  # type: ignore[arg-type]


def test_greeting_ends_with_exclamation_returns_exact_message() -> None:
    assert greeting_ends_with_exclamation("Ada") == "Hello, Ada!"


def test_greeting_ends_with_exclamation_preserves_name_whitespace() -> None:
    assert greeting_ends_with_exclamation(" Ada ") == "Hello,  Ada !"


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greeting_ends_with_exclamation_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_ends_with_exclamation(name)  # type: ignore[arg-type]


def test_greeting_casefold_normalizes_unicode_and_ascii() -> None:
    assert greeting_casefold("Straße") == "hello, strasse"
    assert greeting_casefold("Ada") == "hello, ada"


def test_greeting_casefold_preserves_name_whitespace() -> None:
    assert greeting_casefold(" Straße ") == "hello,  strasse "


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_casefold_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_casefold(name)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("name", "expected"),
    [("Ada", 2), ("Ada Lovelace", 3), (" \tAda\u2003Lovelace\n ", 3)],
)
def test_greeting_word_count_splits_whitespace(name: str, expected: int) -> None:
    assert greeting_word_count(name) == expected


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_word_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_word_count(name)  # type: ignore[arg-type]


def test_greeting_has_semicolon_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada;") == "Hello, Ada;"
    assert greeting_has_semicolon("Ada;") is True


def test_greeting_has_semicolon_reports_absence_in_completed_greeting() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_semicolon("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_semicolon_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_semicolon(name)  # type: ignore[arg-type]


def test_greeting_has_at_sign_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada@") == "Hello, Ada@"
    assert greeting_has_at_sign("Ada@") is True


def test_greeting_has_at_sign_reports_absence_in_completed_greeting() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_at_sign("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_at_sign_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_at_sign(name)  # type: ignore[arg-type]


def test_greeting_has_colon_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada:") == "Hello, Ada:"
    assert greeting_has_colon("Ada:") is True


def test_greeting_has_colon_reports_absence_in_completed_greeting() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_colon("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_colon_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_colon(name)  # type: ignore[arg-type]


def test_greeting_has_question_mark_detects_literal_question_mark() -> None:
    assert greeting_has_question_mark("Ada?") is True


def test_greeting_has_question_mark_reports_absence() -> None:
    assert greeting_has_question_mark("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_question_mark_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_question_mark(name)  # type: ignore[arg-type]


def test_greeting_has_percent_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada%") == "Hello, Ada%"
    assert greeting_has_percent("Ada%") is True


def test_greeting_has_percent_reports_absence() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_percent("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_percent_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_percent(name)  # type: ignore[arg-type]


def test_greeting_has_hash_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada#") == "Hello, Ada#"
    assert greeting_has_hash("Ada#") is True


def test_greeting_has_hash_reports_absence() -> None:
    assert greeting_has_hash("Ada") is False
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_question_mark("Ada?") is True


@pytest.mark.parametrize("name", ["", " ", None, 42])
def test_greeting_has_hash_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_hash(name)  # type: ignore[arg-type]


def test_greeting_has_plus_detects_literal_in_completed_greeting() -> None:
    assert greeting_has_plus("Ada+") is True


def test_greeting_has_plus_reports_absence() -> None:
    assert greeting_has_plus("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_plus_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_plus(name)  # type: ignore[arg-type]


def test_greeting_has_plus_preserves_public_exports() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_hash("Ada#") is True


def test_greeting_has_equal_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada=") == "Hello, Ada="
    assert greeting_has_equal("Ada=") is True


def test_greeting_has_equal_rejects_fullwidth_lookalike() -> None:
    assert greeting_has_equal("Ada") is False
    assert greeting_has_equal("Ada＝") is False


@pytest.mark.parametrize("name", ["", " ", None, 42])
def test_greeting_has_equal_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_equal(name)  # type: ignore[arg-type]


def test_greeting_has_backtick_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada`") == "Hello, Ada`"
    assert greeting_has_backtick("Ada`") is True


def test_greeting_has_backtick_rejects_absence_and_fullwidth_lookalike() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_backtick("Ada") is False
    assert greet("Ada｀") == "Hello, Ada｀"
    assert greeting_has_backtick("Ada｀") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_backtick_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_backtick(name)  # type: ignore[arg-type]


def test_greeting_has_asterisk_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada*") == "Hello, Ada*"
    assert greeting_has_asterisk("Ada*") is True


def test_greeting_has_asterisk_reports_absence() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_asterisk("Ada") is False


def test_greeting_has_asterisk_distinguishes_operator() -> None:
    assert greet("Ada∗") == "Hello, Ada∗"
    assert greeting_has_asterisk("Ada∗") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_asterisk_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_asterisk(name)  # type: ignore[arg-type]


def test_greeting_has_ascii_asterisk_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada*") == "Hello, Ada*"
    assert greeting_has_ascii_asterisk("Ada*") is True


def test_greeting_has_ascii_asterisk_reports_absence() -> None:
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_ascii_asterisk("Ada") is False


@pytest.mark.parametrize("name", ["", " \t\n", None, 42])
def test_greeting_has_ascii_asterisk_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_ascii_asterisk(name)  # type: ignore[arg-type]


def test_greeting_has_ascii_asterisk_preserves_prior_exports() -> None:
    import nmg_sdlc_smoke

    prior = [
        "greet",
        "greet_many",
        "greeting_bytes",
        "greeting_casefold",
        "greeting_ends_with_exclamation",
        "greeting_ends_with_name",
        "greeting_has_asterisk",
        "greeting_has_at_sign",
        "greeting_has_backtick",
        "greeting_has_colon",
        "greeting_has_equal",
        "greeting_has_hash",
        "greeting_has_percent",
        "greeting_has_plus",
        "greeting_has_question_mark",
        "greeting_has_semicolon",
        "greeting_is_ascii",
        "greeting_length",
        "greeting_starts_with_hello",
        "greeting_word_count",
    ]
    assert set(prior) < set(nmg_sdlc_smoke.__all__)
    assert all(callable(getattr(nmg_sdlc_smoke, export)) for export in prior)
    assert greet("Ada") == "Hello, Ada"
    assert greeting_has_asterisk("Ada*") is True


def test_greeting_has_exclamation_detects_literal_in_completed_greeting() -> None:
    assert greet("Ada!") == "Hello, Ada!"
    assert greeting_has_exclamation("Ada!") is True


@pytest.mark.parametrize("name", ["Ada", "Ada！"])
def test_greeting_has_exclamation_reports_absence(name: str) -> None:
    assert "!" not in greet(name)
    assert greeting_has_exclamation(name) is False


@pytest.mark.parametrize("name", ["", " ", None, 42])
def test_greeting_has_exclamation_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_exclamation(name)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("name", "expected"),
    [("Ada!", True), ("Ada?", True), ("Ada!?", True), ("Ada", False), ("Ada\uff01\uff1f", False)],
)
def test_greeting_has_exclamation_or_question_checks_literal_marks(name: str, expected: bool) -> None:
    assert greeting_has_exclamation_or_question(name) is expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_exclamation_or_question_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_exclamation_or_question(name)  # type: ignore[arg-type]


def test_greeting_has_dollar_detects_literal_dollar() -> None:
    assert greet("Ada$") == "Hello, Ada$"
    assert greeting_has_dollar("Ada$") is True


@pytest.mark.parametrize("name", ["Ada", "Ada\uff04"])
def test_greeting_has_dollar_reports_absence(name: str) -> None:
    assert greeting_has_dollar(name) is False


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_dollar_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_dollar(name)  # type: ignore[arg-type]


def test_greeting_has_underscore_detects_literal_underscore() -> None:
    assert greet("Ada_") == "Hello, Ada_"
    assert greeting_has_underscore("Ada_") is True


@pytest.mark.parametrize("name", ["Ada", "Ada\uff3f"])
def test_greeting_has_underscore_reports_absence(name: str) -> None:
    assert greeting_has_underscore(name) is False


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_underscore_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_underscore(name)  # type: ignore[arg-type]


def test_greeting_has_slash_detects_literal_slash() -> None:
    assert greet("Ada/") == "Hello, Ada/"
    assert greeting_has_slash("Ada/") is True


@pytest.mark.parametrize("name", ["Ada", "Ada\uff0f"])
def test_greeting_has_slash_reports_absence(name: str) -> None:
    assert greeting_has_slash(name) is False


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_slash_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_slash(name)  # type: ignore[arg-type]


def test_greeting_has_double_quote_detects_literal_double_quote() -> None:
    assert greet('Ada"') == 'Hello, Ada"'
    assert greeting_has_double_quote('Ada"') is True


@pytest.mark.parametrize("name", ["Ada", "Ada\uff02"])
def test_greeting_has_double_quote_reports_absence(name: str) -> None:
    assert greeting_has_double_quote(name) is False


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_double_quote_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_double_quote(name)  # type: ignore[arg-type]


def test_greeting_has_apostrophe_detects_literal_apostrophe() -> None:
    assert greet("O'Brien") == "Hello, O'Brien"
    assert greeting_has_apostrophe("O'Brien") is True


@pytest.mark.parametrize("name", ["Ada", "O\u2019Brien", "O\u02bcBrien", "O`Brien"])
def test_greeting_has_apostrophe_reports_absence(name: str) -> None:
    assert greeting_has_apostrophe(name) is False


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_apostrophe_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_apostrophe(name)  # type: ignore[arg-type]


def test_greeting_has_backslash_detects_literal_backslash() -> None:
    assert greet("Ada\\") == "Hello, Ada\\"
    assert greeting_has_backslash("Ada\\") is True


@pytest.mark.parametrize("name", ["Ada", "Ada/", "Ada\uff3c", "Ada\u2216"])
def test_greeting_has_backslash_reports_absence(name: str) -> None:
    assert greeting_has_backslash(name) is False


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_has_backslash_preserves_validation(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_has_backslash(name)  # type: ignore[arg-type]


def test_greeting_reversed_reverses_by_code_point() -> None:
    assert greeting_reversed("Ada") == "adA ,olleH"
    assert greeting_reversed("Zo\u00eb") == "\u00eboZ ,olleH"


@pytest.mark.parametrize("name", ["", "   ", None])
def test_greeting_reversed_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_reversed(name)  # type: ignore[arg-type]


def test_greeting_reversed_is_exported_without_dropping_prior_exports() -> None:
    import nmg_sdlc_smoke

    prior = [
        "greet",
        "greet_many",
        "greeting_bytes",
        "greeting_casefold",
        "greeting_ends_with_exclamation",
        "greeting_ends_with_name",
        "greeting_has_apostrophe",
        "greeting_has_ascii_asterisk",
        "greeting_has_asterisk",
        "greeting_has_at_sign",
        "greeting_has_backslash",
        "greeting_has_backtick",
        "greeting_has_colon",
        "greeting_has_dollar",
        "greeting_has_double_quote",
        "greeting_has_equal",
        "greeting_has_exclamation",
        "greeting_has_exclamation_or_question",
        "greeting_has_hash",
        "greeting_has_percent",
        "greeting_has_plus",
        "greeting_has_question_mark",
        "greeting_has_semicolon",
        "greeting_has_slash",
        "greeting_has_underscore",
        "greeting_is_ascii",
        "greeting_length",
        "greeting_starts_with_hello",
        "greeting_word_count",
    ]
    assert "greeting_reversed" in nmg_sdlc_smoke.__all__
    assert set(prior) <= set(nmg_sdlc_smoke.__all__)
    assert greet("Ada") == "Hello, Ada"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 4),
        ("AEIOU aeiou", 12),
        ("Bcd", 2),
        ("Ady", 3),
        ("\u00c9mile", 4),
        ("\uff21\uff44\uff41", 2),
    ],
)
def test_greeting_vowel_count_counts_ascii_vowels(name: str, expected: int) -> None:
    result = greeting_vowel_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_vowel_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_vowel_count(name)  # type: ignore[arg-type]


def test_greeting_vowel_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_vowel_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_vowel_count("Ada") == 4


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 2),
        ("ABC XYZ", 7),
        ("bob 42!", 1),
        ("\u00c9mile", 1),
        ("\uff22\uff23", 1),
    ],
)
def test_greeting_uppercase_count_counts_ascii_capitals(
    name: str, expected: int
) -> None:
    result = greeting_uppercase_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_uppercase_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_uppercase_count(name)  # type: ignore[arg-type]


def test_greeting_uppercase_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_uppercase_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_uppercase_count("Ada") == 2


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 6),
        ("abc xyz", 10),
        ("BOB 42!", 4),
        ("\u00e9", 4),
        ("\uff42\uff43", 4),
    ],
)
def test_greeting_lowercase_count_counts_ascii_lowercase(
    name: str, expected: int
) -> None:
    result = greeting_lowercase_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_lowercase_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_lowercase_count(name)  # type: ignore[arg-type]


def test_greeting_lowercase_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_lowercase_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_lowercase_count("Ada") == 6


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"),
        ("Zo\u00eb", "aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524"),
        ("Zoe\u0308", "af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064"),
    ],
)
def test_greeting_sha256_hashes_utf8_greeting(name: str, expected: str) -> None:
    result = greeting_sha256(name)

    assert type(result) is str
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_sha256_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_sha256(name)  # type: ignore[arg-type]


def test_greeting_sha256_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_sha256" in nmg_sdlc_smoke.__all__
    assert (
        nmg_sdlc_smoke.greeting_sha256("Ada")
        == "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"
    )


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "SGVsbG8sIEFkYQ=="),
        ("a?>", "SGVsbG8sIGE/Pg=="),
        ("a>>", "SGVsbG8sIGE+Pg=="),
        ("Bo", "SGVsbG8sIEJv"),
        ("Bob~", "SGVsbG8sIEJvYn4="),
        ("Zo\u00eb", "SGVsbG8sIFpvw6s="),
        ("Zoe\u0308", "SGVsbG8sIFpvZcyI"),
        (
            "A" * 60,
            (
                "SGVsbG8sIEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
                "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQQ=="
            ),
        ),
    ],
)
def test_greeting_base64_encodes_utf8_greeting(name: str, expected: str) -> None:
    result = greeting_base64(name)

    assert type(result) is str
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_base64_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_base64(name)  # type: ignore[arg-type]


def test_greeting_base64_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_base64" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_base64("Ada") == "SGVsbG8sIEFkYQ=="


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "Uryyb, Nqn"),
        ("Mary-Jane O'Neil", "Uryyb, Znel-Wnar B'Arvy"),
        ("Zo\u00eb", "Uryyb, Mb\u00eb"),
        ("\uff3aed 42", "Uryyb, \uff3arq 42"),
    ],
)
def test_greeting_rot13_rotates_ascii_letters(name: str, expected: str) -> None:
    result = greeting_rot13(name)

    assert type(result) is str
    assert result == expected
    assert codecs.encode(result, "rot13") == greet(name)


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_rot13_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_rot13(name)  # type: ignore[arg-type]


def test_greeting_rot13_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_rot13" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_rot13("Ada") == "Uryyb, Nqn"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("R2D2", 2),
        ("Agent 007", 3),
        ("Ada", 0),
        ("\uff11\uff12", 0),
        ("\u0663", 0),
        ("x\u00b2", 0),
    ],
)
def test_greeting_digit_count_counts_ascii_digits(name: str, expected: int) -> None:
    result = greeting_digit_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_digit_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_digit_count(name)  # type: ignore[arg-type]


def test_greeting_digit_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_digit_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_digit_count("R2D2") == 2


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 1),
        ("Ada Lovelace", 2),
        ("Grace Brewster Hopper", 3),
        ("Ada\tLovelace", 1),
        ("Ada\nLovelace", 1),
        ("Ada\u00a0Lovelace", 1),
    ],
)
def test_greeting_space_count_counts_ascii_spaces(name: str, expected: int) -> None:
    result = greeting_space_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_space_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_space_count(name)  # type: ignore[arg-type]


def test_greeting_space_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_space_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_space_count("Ada Lovelace") == 2


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 1),
        ("O'Brien", 2),
        ("Ada!?", 3),
        ("a.b-c_d", 4),
        ("Ada！", 1),
        ("O’Brien", 1),
        ("Ada、", 1),
        ("Ada Lovelace 42", 1),
    ],
)
def test_greeting_punctuation_count_counts_ascii_punctuation(
    name: str, expected: int
) -> None:
    result = greeting_punctuation_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_punctuation_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_punctuation_count(name)  # type: ignore[arg-type]


def test_greeting_punctuation_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_punctuation_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_punctuation_count("O'Brien") == 2


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 9),
        ("Bob", 8),
        ("Ada Lovelace", 12),
        ("ADA", 8),
        ("Zoë", 8),
    ],
)
def test_greeting_unique_char_count_counts_distinct_code_points(
    name: str, expected: int
) -> None:
    result = greeting_unique_char_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_unique_char_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_unique_char_count(name)  # type: ignore[arg-type]


def test_greeting_unique_char_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_unique_char_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_unique_char_count("Ada") == 9


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "Hello%2C%20Ada"),
        ("A/B&C~d_e.f", "Hello%2C%20A%2FB%26C~d_e.f"),
        ("Zoë", "Hello%2C%20Zo%C3%AB"),
    ],
)
def test_greeting_url_encoded_percent_encodes_utf8_greeting(
    name: str, expected: str
) -> None:
    result = greeting_url_encoded(name)

    assert type(result) is str
    assert result == expected
    assert unquote(result) == greet(name)


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_url_encoded_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_url_encoded(name)  # type: ignore[arg-type]


def test_greeting_url_encoded_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_url_encoded" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_url_encoded("Ada") == "Hello%2C%20Ada"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 8),
        ("Ada Lovelace", 16),
        ("R2D2", 7),
        ("Zoë", 8),
        ("O'Brien", 11),
    ],
)
def test_greeting_letter_count_counts_alphabetic_characters(
    name: str, expected: int
) -> None:
    result = greeting_letter_count(name)

    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_letter_count_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_letter_count(name)  # type: ignore[arg-type]


def test_greeting_letter_count_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_letter_count" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_letter_count("Ada") == 8


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 2761732226),
        ("Ada Lovelace", 2495651459),
        ("Zoë", 2271742533),
    ],
)
def test_greeting_crc32_returns_unsigned_checksum(name: str, expected: int) -> None:
    result = greeting_crc32(name)

    assert type(result) is int
    assert result == expected


def test_greeting_crc32_checksums_utf8_encoding() -> None:
    greeting = "Hello, Zoë"

    assert greeting_crc32("Zoë") == zlib.crc32(greeting.encode("utf-8"))


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_crc32_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_crc32(name)  # type: ignore[arg-type]


def test_greeting_crc32_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_crc32" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_crc32("Ada") == 2761732226


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", 312279879),
        ("Ada Lovelace", 1063257746),
        ("Zoë", 400032888),
    ],
)
def test_greeting_adler32_returns_unsigned_checksum(name: str, expected: int) -> None:
    result = greeting_adler32(name)

    assert type(result) is int
    assert result == expected


def test_greeting_adler32_checksums_utf8_encoding() -> None:
    greeting = "Hello, Zoë"

    assert greeting_adler32("Zoë") == zlib.adler32(greeting.encode("utf-8"))


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_adler32_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_adler32(name)  # type: ignore[arg-type]


def test_greeting_adler32_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_adler32" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_adler32("Ada") == 312279879


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "a4f502ca98cce831af61b0fe0a319382"),
        ("Ada Lovelace", "bd0b2e5ea5baf6775e93262ce37d5a4a"),
        ("Zoë", "26ed66c6559b1e033c70ef2301fe0beb"),
    ],
)
def test_greeting_md5_returns_hex_digest(name: str, expected: str) -> None:
    result = greeting_md5(name)

    assert type(result) is str
    assert result == expected


def test_greeting_md5_hashes_utf8_encoding() -> None:
    greeting = "Hello, Zoë"

    assert greeting_md5("Zoë") == hashlib.md5(greeting.encode("utf-8")).hexdigest()


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_md5_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_md5(name)  # type: ignore[arg-type]


def test_greeting_md5_is_exported() -> None:
    import nmg_sdlc_smoke

    assert "greeting_md5" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_md5("Ada") == "a4f502ca98cce831af61b0fe0a319382"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "991f190147e71279d8656214e556b36a22bf73e4"),
        ("Ada Lovelace", "8dde18c21e3195df968018b6213efc61d033ec4f"),
        ("Zoë", "5e2bef193596dd46528fb36c4ef8625f71c84577"),
    ],
)
def test_greeting_sha1_returns_hex_digest(name: str, expected: str) -> None:
    result = greeting_sha1(name)

    assert type(result) is str
    assert result == expected


def test_greeting_sha1_hashes_utf8_encoding() -> None:
    greeting = "Hello, Zoë"

    assert greeting_sha1("Zoë") == hashlib.sha1(greeting.encode("utf-8")).hexdigest()


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_sha1_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_sha1(name)  # type: ignore[arg-type]


def test_greeting_sha1_is_exported() -> None:
    import nmg_sdlc_smoke

    expected = "991f190147e71279d8656214e556b36a22bf73e4"

    assert "greeting_sha1" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_sha1("Ada") == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "8abfe44c9cccb8990fcecac86c840fce7ccb1949a4eb49569c0f0cedc1481a8cdac6a37dd286d2d1d8175ebd63ff071b8882052d0a0bd874f88e03ad812215e2"),
        ("Ada Lovelace", "6c200b8221e61ef4fa3e4028a8484253f8abf94b0034d52be2224f37d7039c7b081304d248d8b6424c7455c1dac951ddd61968721ef9969f43fb36ea87abbb53"),
        ("Zoë", "f93e61e8fa95d7f3f732ba7cd41ab19b7b2bbee43b20e1f1aca2c7ffeac6d39444bbaec839b5cd2e7e5dbc5adb4c651d3c65fa1fb3765fd5cde55509fe5b2e59"),
    ],
)
def test_greeting_sha512_returns_hex_digest(name: str, expected: str) -> None:
    result = greeting_sha512(name)

    assert type(result) is str
    assert result == expected


def test_greeting_sha512_hashes_utf8_encoding() -> None:
    greeting = "Hello, Zoë"

    assert greeting_sha512("Zoë") == hashlib.sha512(greeting.encode("utf-8")).hexdigest()


@pytest.mark.parametrize("name", ["", " \t", None, 42])
def test_greeting_sha512_rejects_invalid_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greeting_sha512(name)  # type: ignore[arg-type]


def test_greeting_sha512_is_exported() -> None:
    import nmg_sdlc_smoke

    expected = "8abfe44c9cccb8990fcecac86c840fce7ccb1949a4eb49569c0f0cedc1481a8cdac6a37dd286d2d1d8175ebd63ff071b8882052d0a0bd874f88e03ad812215e2"

    assert "greeting_sha512" in nmg_sdlc_smoke.__all__
    assert nmg_sdlc_smoke.greeting_sha512("Ada") == expected
