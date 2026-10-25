# nmg-sdlc-smoke-python

A disposable Python SDLC smoke host used to exercise issue-to-spec-to-delivery workflows against a small, independently verifiable project.

## Requirements

- Python 3.12 or newer
- `VERSION` is the release source of truth; `pyproject.toml` reads it dynamically

## Install

```console
python -m pip install -e ".[dev]"
```

## Library

```python
from nmg_sdlc_smoke import (
    greet,
    greet_many,
    greeting_adler32,
    greeting_base32,
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
    greeting_sha224,
    greeting_sha256,
    greeting_sha384,
    greeting_sha3_224,
    greeting_sha3_256,
    greeting_sha3_384,
    greeting_sha3_512,
    greeting_sha512,
    greeting_space_count,
    greeting_starts_with_hello,
    greeting_url_encoded,
    greeting_unique_char_count,
    greeting_uppercase_count,
    greeting_vowel_count,
    greeting_word_count,
)

greet("Ada")  # "Hello, Ada"
greeting_ends_with_exclamation("Ada")  # "Hello, Ada!"
greet_many(["Ada", "Bob"])  # ["Hello, Ada", "Hello, Bob"]
greeting_length("Ada")  # 10
greeting_bytes("Ada")  # 10
greeting_is_ascii("Ada")  # True
greeting_casefold("Straße")  # "hello, strasse"
greeting_reversed("Ada")  # "adA ,olleH"
greeting_starts_with_hello("Ada")  # True
greeting_ends_with_name("Ada")  # True
greeting_has_apostrophe("O'Brien")  # True
greeting_has_apostrophe("Ada")  # False
greeting_has_apostrophe("O’Brien")  # False
greeting_has_ascii_asterisk("Ada*")  # True
greeting_has_ascii_asterisk("Ada")  # False
greeting_has_asterisk("Ada*")  # True
greeting_has_asterisk("Ada")  # False
greeting_has_asterisk("Ada∗")  # False
greeting_has_backslash("Ada\\")  # True
greeting_has_backslash("Ada")  # False
greeting_has_backtick("Ada`")  # True
greeting_has_backtick("Ada")  # False
greeting_has_backtick("Ada｀")  # False
greeting_has_at_sign("Ada@")  # True
greeting_has_at_sign("Ada")  # False
greeting_has_colon("Ada:")  # True
greeting_has_colon("Ada")  # False
greeting_has_dollar("Ada$")  # True
greeting_has_dollar("Ada")  # False
greeting_has_double_quote('Ada"')  # True
greeting_has_double_quote("Ada")  # False
greeting_has_equal("Ada=")  # True
greeting_has_equal("Ada")  # False
greeting_has_equal("Ada＝")  # False
greeting_has_exclamation("Ada!")  # True
greeting_has_exclamation("Ada")  # False
greeting_has_exclamation_or_question("Ada!")  # True
greeting_has_exclamation_or_question("Ada?")  # True
greeting_has_exclamation_or_question("Ada")  # False
greeting_has_hash("Ada#")  # True
greeting_has_hash("Ada")  # False
greeting_has_percent("Ada%")  # True
greeting_has_percent("Ada")  # False
greeting_has_plus("Ada+")  # True
greeting_has_plus("Ada")  # False
greeting_has_question_mark("Ada?")  # True
greeting_has_question_mark("Ada")  # False
greeting_has_semicolon("Ada;")  # True
greeting_has_semicolon("Ada")  # False
greeting_has_slash("Ada/")  # True
greeting_has_slash("Ada")  # False
greeting_has_underscore("Ada_")  # True
greeting_has_underscore("Ada")  # False
greeting_word_count("Ada")  # 2
greeting_word_count("Ada Lovelace")  # 3
greeting_vowel_count("Ada")  # 4
greeting_uppercase_count("Ada")  # 2
greeting_lowercase_count("Ada")  # 6
greeting_digit_count("R2D2")  # 2
greeting_space_count("Ada Lovelace")  # 2
greeting_punctuation_count("O'Brien")  # 2
greeting_unique_char_count("Ada")  # 9
greeting_letter_count("Ada")  # 8
greeting_sha256("Ada")  # "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"
greeting_md5("Ada")  # "a4f502ca98cce831af61b0fe0a319382"
greeting_sha1("Ada")  # "991f190147e71279d8656214e556b36a22bf73e4"
greeting_sha512("Ada")  # "8abfe44c9cccb8990fcecac86c840fce7ccb1949a4eb49569c0f0cedc1481a8cdac6a37dd286d2d1d8175ebd63ff071b8882052d0a0bd874f88e03ad812215e2"
greeting_sha384("Ada")  # "81cbed2fa5e07b7ec1d2a13da4de9584c07ddbbb2748dc5711aaafb067c07b03c120099ddcd53135b382c0e3c6198f5d"
greeting_sha224("Ada")  # "316233754fcc3ee5160b0102d33639e694a894f689633ca5d2d679ad"
greeting_sha3_224("Ada")  # "4f8b1b1e2d62e0fc1292bbc88641b8883bcccc2d0087052131c359aa"
greeting_sha3_256("Ada")  # "8fe4a55d0487c2a730a2f841a99b44d01ca1f235c30ab3a452af08ca7cd531d4"
greeting_sha3_384("Ada")  # "1a0e27fabec84a7b6ff60b8feb3cb3a8f6c3838c4242005c74f61de0149c524ac44e5f4d417d35726285bd9ee10b470b"
greeting_sha3_512("Ada")  # "0817552f59fade788cc6bfaff1161167b75c5f73a5c0f314be498ad984301ae1a4adf9b9770cd68d4af5d3093d061a5e3b6b306117803a6f359d98cb862a8611"
greeting_base64("Ada")  # "SGVsbG8sIEFkYQ=="
greeting_base32("Ada")  # "JBSWY3DPFQQECZDB"
greeting_url_encoded("Ada")  # "Hello%2C%20Ada"
greeting_rot13("Ada")  # "Uryyb, Nqn"
greeting_crc32("Ada")  # 2761732226
greeting_adler32("Ada")  # 312279879
```

`greet` rejects blank, whitespace-only, and non-string names with `ValueError("name must not be blank")`.
`greeting_casefold` applies Unicode casefolding to the complete greeting and uses the same validation as `greet`; it does not change `greet` or CLI output.
`greeting_reversed` reverses the complete greeting by Unicode code point (not by grapheme cluster) and uses the same validation as `greet`; it does not change `greet` or CLI output.
`greeting_word_count` counts whitespace-separated words in the complete greeting using Python's `str.split()` semantics and the same validation as `greet`.
`greeting_vowel_count` counts the ten ASCII vowels `a e i o u A E I O U` in the complete greeting (not the name alone); `y`, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_uppercase_count` counts the 26 ASCII capitals `A`–`Z` in the complete greeting (not the name alone), including the `H` in `Hello`; lowercase, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_lowercase_count` counts the 26 ASCII lowercase letters `a`–`z` in the complete greeting (not the name alone), including the `ello` in `Hello`; uppercase, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_digit_count` counts the ten ASCII digits `0`–`9` in the complete greeting (not the name alone); fullwidth, other-script, and superscript digits are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_space_count` counts the ASCII space U+0020 in the complete greeting (not the name alone), including the space after `Hello,`; tabs, newlines, no-break spaces, and other Unicode whitespace are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_punctuation_count` counts the 32 ASCII punctuation characters in Python's `string.punctuation` in the complete greeting (not the name alone), including the comma after `Hello`; non-ASCII punctuation and look-alikes such as `！`, `’`, and `、` are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_unique_char_count` counts the distinct Unicode code points in the complete greeting (not the name alone), including the characters of `Hello, `; the count is case-sensitive and applies no Unicode normalization, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_letter_count` counts the characters in the complete greeting (not the name alone) for which `str.isalpha()` is true, including the five letters of `Hello`; non-ASCII letters such as `ë` are counted, while digits, spaces, and punctuation are not, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha256` encodes the complete greeting (not the name alone) as UTF-8 and returns its SHA-256 digest as 64 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_md5` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its MD5 digest from `hashlib.md5` as 32 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha1` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-1 digest from `hashlib.sha1` as 40 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha512` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-512 digest from `hashlib.sha512` as 128 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha384` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-384 digest from `hashlib.sha384` as 96 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha224` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-224 digest from `hashlib.sha224` as 56 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha3_224` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA3-224 digest from `hashlib.sha3_224` as 56 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha3_256` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA3-256 digest from `hashlib.sha3_256` as 64 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha3_384` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA3-384 digest from `hashlib.sha3_384` as 96 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_sha3_512` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA3-512 digest from `hashlib.sha3_512` as 128 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_base64` encodes the complete greeting (not the name alone) as UTF-8 and returns its standard Base64 encoding as a `str`, using the RFC 4648 alphabet with `+` and `/`, `=` padding, and no line breaks; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_base32` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its standard Base32 encoding from `base64.b32encode` as a `str`, using the RFC 4648 alphabet of uppercase `A`–`Z` and `2`–`7`, `=` padding, and no line breaks; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_rot13` applies ROT13 to the complete greeting (not the name alone), rotating only the ASCII letters `A`–`Z` and `a`–`z` by 13 places within their case and leaving every other character, including non-ASCII letters, unchanged; applying ROT13 again restores the greeting, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_url_encoded` percent-encodes the complete greeting (not the name alone) as UTF-8 with uppercase hex digits, leaving only `A`–`Z`, `a`–`z`, `0`–`9`, `-`, `.`, `_`, and `~` unencoded (so a space becomes `%20` and `/` becomes `%2F`); `urllib.parse.unquote` restores the greeting, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_crc32` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its unsigned CRC-32 checksum from `zlib.crc32` as an `int` between `0` and `4294967295`; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different checksums, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_adler32` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its unsigned Adler-32 checksum from `zlib.adler32` as an `int` between `0` and `4294967295`; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different checksums, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_semicolon` checks for a literal `;` in the complete greeting and uses the same name validation as `greet`.
`greeting_has_colon` checks for a literal `:` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_dollar` checks for a literal `$` in the complete greeting (not the fullwidth `＄`) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_double_quote` checks for a literal `"` in the complete greeting (not the fullwidth `＂`) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_underscore` checks for a literal `_` (U+005F) in the completed greeting (not the fullwidth `＿`) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_ascii_asterisk` checks for a literal ASCII `*` in the completed greeting and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_asterisk` matches only a literal ASCII `*` (U+002A) in the completed greeting, not U+2217 `∗`, and inherits `greet`'s `ValueError("name must not be blank")`.
`greeting_has_backtick` matches only a literal ASCII backtick (U+0060) in the complete greeting, not the fullwidth lookalike U+FF40, and inherits `greet`'s `ValueError("name must not be blank")`.

`greeting_has_backslash` matches only a literal ASCII backslash `\` (U+005C) in the completed greeting, not `/` (U+002F), the fullwidth `＼` (U+FF3C), or `∖` (U+2216), and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_at_sign` checks for a literal `@` in the completed greeting and uses the same name validation as `greet`.
`greeting_has_equal` matches only a literal ASCII `=` in the complete greeting (not a fullwidth `＝`) and inherits `greet`'s invalid-name `ValueError`.
`greeting_has_exclamation` checks for a literal `!` in the completed greeting (not the fullwidth `！`) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_exclamation_or_question` checks whether the completed greeting contains a literal `!` or `?` (not the fullwidth `！` or `？`) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_hash` checks for a literal `#` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_question_mark` checks for a literal `?` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_percent` checks for a literal `%` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_plus` checks for a literal `+` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_slash` checks for a literal `/` in the complete greeting (not the fullwidth `／`) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
`greeting_has_apostrophe` checks for a literal ASCII `'` (U+0027) in the completed greeting (not `’` U+2019, `ʼ` U+02BC, or `` ` `` U+0060) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.

## CLI

```console
$ nmg-smoke Ada
Hello, Ada
```

Use `--uppercase` to capitalize the complete greeting:

```console
$ nmg-smoke --uppercase Ada
HELLO, ADA
```

Use `--lowercase` to lowercase the complete greeting:

```console
$ nmg-smoke --lowercase Ada
hello, ada
```

Lowercasing uses Python `str.lower()` and applies before the literal prefix, so
prefix text keeps its original case. Combining `--lowercase` with `--uppercase`
is rejected with exit status 2.

Use `--swapcase` to invert the letter case of the complete greeting:

```console
$ nmg-smoke --swapcase Ada
hELLO, aDA
```

Case swapping uses Python `str.swapcase()` and applies before the literal
prefix, so prefix text keeps its original case. Combining `--swapcase` with
`--uppercase` or `--lowercase` is rejected with exit status 2.

Use `--titlecase` to title-case the complete greeting:

```console
$ nmg-smoke --titlecase ada
Hello, Ada
```

Title-casing uses Python `str.title()` and applies before the literal prefix,
so prefix text keeps its original case. Combining `--titlecase` with
`--uppercase`, `--lowercase`, or `--swapcase` is rejected with exit status 2.

Use `--casefold` to casefold the complete greeting for caseless comparison:

```console
$ nmg-smoke --casefold Straße
hello, strasse
```

Casefolding uses Python `str.casefold()` and applies before the literal prefix,
so prefix text keeps its original case. Combining `--casefold` with
`--uppercase`, `--lowercase`, `--swapcase`, or `--titlecase` is rejected with
exit status 2.

Use `--repeat COUNT` to print the greeting once per line:

```console
$ nmg-smoke --repeat 3 Ada
Hello, Ada
Hello, Ada
Hello, Ada
```

Use `--prefix TEXT` to prepend text exactly as supplied:

```console
$ nmg-smoke --prefix 'OK: ' Ada
OK: Hello, Ada
```

Use `--no-newline` to omit the trailing newline from successful output:

```console
$ nmg-smoke --no-newline Ada
Hello, Ada
```

The output above is exactly `Hello, Ada` without a trailing newline.

Use `--parentheses` to enclose each fully composed greeting in literal parentheses:

```console
$ nmg-smoke --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada
(ok: HELLO, ADA)
(ok: HELLO, ADA)
```

Uppercase applies before the literal prefix; parentheses wrap the complete message
once before repetition and newline handling. The example has one separating LF
and no final LF. Existing parentheses and internal newlines are preserved without
escaping. Without `--parentheses`, composed and default output remain unchanged.

Use `--braces` to enclose each fully formatted greeting in literal curly braces:

```console
$ nmg-smoke --braces --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada
{(ok: HELLO, ADA)}
{(ok: HELLO, ADA)}
```

Braces wrap the complete message after parentheses and before repetition and
newline handling, so they are always outermost. Without `--braces`, composed
and default output remain byte-identical.

Use `--quotes` to enclose the fully composed greeting in literal double quotes:

```console
$ nmg-smoke --quotes --uppercase --prefix 'ok: ' --parentheses --braces Ada
"{(ok: HELLO, ADA)}"
```

Quotes wrap the complete message after braces and before repetition and newline
handling. Without `--quotes`, output remains byte-identical.

A blank name exits 1 and writes no greeting to stdout.

## Verification

```console
python -m pytest
python -m pytest tests/features
python -m ruff check .
```

Unit tests cover the library and CLI. pytest-bdd scenarios under `tests/features/` cover the approved acceptance criteria. Ruff checks `src/` and `tests/`. GitHub Actions runs the same Python checks on pull requests and pushes to `main`.

## Layout

- `src/nmg_sdlc_smoke/` — import package and console entry point
- `tests/` — pytest unit tests
- `tests/features/` — pytest-bdd features and steps
- `specs/` — current approved issue contracts
- `steering/` — product, technology, and structure guidance
- `VERSION` — 3.x version source synchronized into package metadata

This repository is intentionally minimal. Git history, not the working tree, archives the copied plugin that preceded the Python host.
