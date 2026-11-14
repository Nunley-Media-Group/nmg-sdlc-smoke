Feature: Report whether the completed greeting is printable

  @SCN001
  Scenario: Report True for fully printable greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_is_printable is called with Ada, Zo plus U+00EB, and Ada Lovelace
    Then each result is the bool True
    And each result equals the isprintable result of the greeting

  @SCN002
  Scenario: Report False when the greeting contains a non-printable character
    Given the installed nmg_sdlc_smoke package
    When greeting_is_printable is called with Ada tab Lovelace and Ada with a trailing newline
    Then each result is the bool False
    And each result equals the isprintable result of the greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_is_printable is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_is_printable of Ada
    Then it prints True and greeting_is_printable is listed in nmg_sdlc_smoke.__all__
    And the README documents the printable check on the complete greeting and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
