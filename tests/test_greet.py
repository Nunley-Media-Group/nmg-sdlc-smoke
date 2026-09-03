import pytest

from nmg_sdlc_smoke import (
    greet,
    greet_many,
    greeting_bytes,
    greeting_ends_with_name,
    greeting_is_ascii,
    greeting_length,
    greeting_starts_with_hello,
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
