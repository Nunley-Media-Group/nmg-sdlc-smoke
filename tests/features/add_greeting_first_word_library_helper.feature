Feature: Return the first word of the completed greeting

  @SCN001
  Scenario: Return the first word for single- and multi-word names
    Given the installed nmg_sdlc_smoke package
    When greeting_first_word is called with Ada, Ada Lovelace, and Agent 007
    Then each result is Hello comma
    And each result is a str

  @SCN002
  Scenario: Split on any whitespace and keep the word unchanged
    Given the installed nmg_sdlc_smoke package
    When greeting_first_word is called with Ada tab Lovelace, space Ada space, and Chloe plus U+0301
    Then each result is Hello comma with 6 code points

  @SCN003
  Scenario: Agree with greeting_words
    Given the installed nmg_sdlc_smoke package
    When greeting_first_word is called with Ada, Ada Lovelace, Agent 007, Ada tab Lovelace, space Ada space, and Chloe plus U+0301
    Then each result equals the first element of greeting_words of the same name

  @SCN004
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_first_word is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN005
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints greeting_first_word of Ada Lovelace
    Then it prints Hello comma and greeting_first_word is listed in nmg_sdlc_smoke.__all__
    And the README documents the first-word rule and the inherited invalid-name error
