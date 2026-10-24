Feature: Count ASCII punctuation in the completed greeting

  @SCN001
  Scenario: Count ASCII punctuation in the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_punctuation_count is called with Ada, O'Brien, Ada!?, and a.b-c_d
    Then the results are the Python int values 1, 2, 3, and 4

  @SCN002
  Scenario: Ignore non-ASCII look-alikes and non-punctuation characters
    Given the installed nmg_sdlc_smoke package
    When greeting_punctuation_count is called with Ada plus U+FF01, O U+2019 Brien, Ada plus U+3001, and Ada Lovelace 42
    Then the results are 1, 1, 1, and 1

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_punctuation_count is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_punctuation_count of O'Brien
    Then it prints 2 and greeting_punctuation_count is listed in nmg_sdlc_smoke.__all__
    And the README documents the ASCII string.punctuation set, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
