Feature: Count ASCII lowercase letters in the completed greeting

  @SCN001
  Scenario: Count ASCII lowercase letters in the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_lowercase_count is called with Ada and with abc xyz
    Then the results are the Python int values 6 and 10

  @SCN002
  Scenario: Count only the 26 ASCII lowercase letters
    Given the installed nmg_sdlc_smoke package
    When greeting_lowercase_count is called with BOB 42!, precomposed U+00E9, and fullwidth U+FF42 U+FF43
    Then the results are 4, 4, and 4

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_lowercase_count is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_lowercase_count of Ada
    Then it prints 6 and greeting_lowercase_count is listed in nmg_sdlc_smoke.__all__
    And the README documents the ASCII a-z set, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
