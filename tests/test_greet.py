import pytest

from nmg_sdlc_smoke import greet, greeting_length


def test_greet_returns_exact_message() -> None:
    assert greet("Ada") == "Hello, Ada"


@pytest.mark.parametrize("name", ["", " ", "\t", "\n", None, 42])
def test_greet_rejects_blank_and_non_string_names(name: object) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet(name)  # type: ignore[arg-type]


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
