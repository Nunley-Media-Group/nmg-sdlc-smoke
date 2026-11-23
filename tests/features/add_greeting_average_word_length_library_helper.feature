Feature: Return the average word length of the completed greeting

  @SCN001
  Scenario: Return the mean word length for simple and multi-word greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_average_word_length is called with Ada, Ada Lovelace, and Agent 007
    Then the results are 4.5, then 17 / 3, then 14 / 3
    And each result is a float

  @SCN002
  Scenario: Return a float when the mean is a whole number
    Given the installed nmg_sdlc_smoke package
    When greeting_average_word_length is called with Bertha
    Then the result is 6.0
    And the result is a float

  @SCN003
  Scenario: Split on any whitespace
    Given the installed nmg_sdlc_smoke package
    When greeting_average_word_length is called with Ada tab Lovelace, space Ada space, and Bo two-spaces Al
    Then the results are 17 / 3, then 4.5, then 10 / 3

  @SCN004
  Scenario: Measure code points without normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_average_word_length is called with Chlo plus U+00E9, and Chloe plus U+0301
    Then the results are 5.5 and 6.0

  @SCN005
  Scenario: Agree with the existing word helpers
    Given the installed nmg_sdlc_smoke package
    When greeting_average_word_length is called with Ada, Ada Lovelace, Agent 007, Bertha, Bo Al, O'Brien-Smith, and Chloe plus U+0301
    Then each result equals the sum of greeting_word_lengths divided by the number of greeting_words of the same name
    And each result lies between the shortest and longest word lengths of the same name

  @SCN006
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_average_word_length is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN007
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_average_word_length of Ada
    Then it prints 4.5 and greeting_average_word_length is listed in nmg_sdlc_smoke.__all__
    And the README documents the average-word-length rule and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
