Feature: Report whether the completed greeting is title-cased

  @SCN001
  Scenario: Report True for title-cased greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_is_title is called with Ada, Zo plus U+00EB, Ada Lovelace, and O'Neil
    Then each result is the bool True
    And each result equals the istitle result of the greeting

  @SCN002
  Scenario: Report False for greetings that are not title-cased
    Given the installed nmg_sdlc_smoke package
    When greeting_is_title is called with ada, ADA, Ada lovelace, and McAdam
    Then each result is the bool False
    And each result equals the istitle result of the greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_is_title is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_is_title of Ada
    Then it prints True and greeting_is_title is listed in nmg_sdlc_smoke.__all__
    And the README documents the title-case check on the complete greeting and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
