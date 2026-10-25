Feature: Count alphabetic characters in the completed greeting

  @SCN001
  Scenario: Count alphabetic characters in the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_letter_count is called with Ada, Ada Lovelace, and R2D2
    Then the results are the Python int values 8, 16, and 7

  @SCN002
  Scenario: Count Unicode letters and exclude non-letters
    Given the installed nmg_sdlc_smoke package
    When greeting_letter_count is called with Zo plus U+00EB and O'Brien
    Then the results are 8 and 11

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_letter_count is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_letter_count of Ada
    Then it prints 8 and greeting_letter_count is listed in nmg_sdlc_smoke.__all__
    And the README documents the isalpha letter rule, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
