Feature: Return the longest word of the completed greeting

  @SCN001
  Scenario: Return the longest word for simple and multi-word greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_longest_word is called with Ada, Ada Lovelace, and Agent 007
    Then the results are Hello, then Lovelace, then Hello,
    And each result is a plain str

  @SCN002
  Scenario: Return the first word on a length tie
    Given the installed nmg_sdlc_smoke package
    When greeting_longest_word is called with Bertha
    Then the result is the first six-character word Hello,

  @SCN003
  Scenario: Split on any whitespace
    Given the installed nmg_sdlc_smoke package
    When greeting_longest_word is called with Ada tab Lovelace, space Ada space, and Ada two-spaces Lovelace
    Then the results are Lovelace, then Hello,, then Lovelace

  @SCN004
  Scenario: Measure code points without normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_longest_word is called with Chlo plus U+00E9 plus e, and Chloe plus U+0301 plus e
    Then the results are Hello, and the unchanged decomposed name

  @SCN005
  Scenario: Agree with the existing word helpers
    Given the installed nmg_sdlc_smoke package
    When greeting_longest_word is called with Ada, Ada Lovelace, Agent 007, Bertha, O'Brien-Smith, and Chloe plus U+0301 plus e
    Then each result is one of greeting_words of the same name
    And each result is as long as the maximum of greeting_word_lengths of the same name

  @SCN006
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_longest_word is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN007
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_longest_word of Ada
    Then it prints Hello, and greeting_longest_word is listed in nmg_sdlc_smoke.__all__
    And the README documents the longest-word rule and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
