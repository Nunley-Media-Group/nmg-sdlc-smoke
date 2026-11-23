Feature: Return the last word of the completed greeting

  @SCN001
  Scenario: Return the last word for single- and multi-word names
    Given the installed nmg_sdlc_smoke package
    When greeting_last_word is called with Ada, Ada Lovelace, and Agent 007
    Then the results are Ada, then Lovelace, then 007
    And each result is a str

  @SCN002
  Scenario: Split on any whitespace
    Given the installed nmg_sdlc_smoke package
    When greeting_last_word is called with Ada tab Lovelace, space Ada space, and Bo two-spaces Al newline
    Then the results are Lovelace, then Ada, then Al

  @SCN003
  Scenario: Return the word unchanged
    Given the installed nmg_sdlc_smoke package
    When greeting_last_word is called with Ada!, O'Brien-Smith, and Chloe plus U+0301
    Then the results are Ada!, then O'Brien-Smith, then Chloe plus U+0301 with 6 code points

  @SCN004
  Scenario: Agree with greeting_words
    Given the installed nmg_sdlc_smoke package
    When greeting_last_word is called with Ada, Ada Lovelace, Agent 007, Ada tab Lovelace, O'Brien-Smith, and Chloe plus U+0301
    Then each result equals the last element of greeting_words of the same name

  @SCN005
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_last_word is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN006
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints greeting_last_word of Ada Lovelace
    Then it prints Lovelace and greeting_last_word is listed in nmg_sdlc_smoke.__all__
    And the README documents the last-word rule and the inherited invalid-name error
