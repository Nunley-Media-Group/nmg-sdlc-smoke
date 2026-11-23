Feature: Count the words of the completed greeting

  @SCN001
  Scenario: Count words in first-seen order
    Given the installed nmg_sdlc_smoke package
    When greeting_word_frequency is called with Ada, Ada Lovelace, and Bo Bo
    Then the results are Hello, 1 Ada 1, then Hello, 1 Ada 1 Lovelace 1, then Hello, 1 Bo 2
    And each result is a dict with keys in first-seen order

  @SCN002
  Scenario: Split on any whitespace
    Given the installed nmg_sdlc_smoke package
    When greeting_word_frequency is called with Bo tab Bo, space Ada space, and Bo two-spaces Al newline Bo
    Then the results are Hello, 1 Bo 2, then Hello, 1 Ada 1, then Hello, 1 Bo 2 Al 1

  @SCN003
  Scenario: Keep words exact
    Given the installed nmg_sdlc_smoke package
    When greeting_word_frequency is called with Bo bo, Hello Hello comma, and Chloe plus U+0301 space Chlo plus U+00E9
    Then the results are Hello, 1 Bo 1 bo 1, then Hello, 2 Hello 1, then Hello, 1 with each Chloe spelling counted separately

  @SCN004
  Scenario: Agree with the existing word helpers
    Given the installed nmg_sdlc_smoke package
    When greeting_word_frequency is called with Ada, Bo Bo, Bo two-spaces Al newline Bo, O'Brien-Smith, and Hello Hello comma
    Then each result's values sum to greeting_word_count of the same name
    And each result's keys equal greeting_words of the same name with later duplicates removed

  @SCN005
  Scenario: Return a new dict on each call
    Given the installed nmg_sdlc_smoke package
    When greeting_word_frequency is called twice with Ada and the first result is mutated
    Then the second result is Hello, 1 Ada 1 and is a different object

  @SCN006
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_word_frequency is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN007
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints greeting_word_frequency of Bo Bo
    Then it prints the Hello, 1 Bo 2 dict and greeting_word_frequency is listed in nmg_sdlc_smoke.__all__
    And the README documents the word-frequency rule and the inherited invalid-name error
