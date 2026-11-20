Feature: Report the length of each word of the completed greeting

  @SCN001
  Scenario: Return per-word lengths for simple and multi-word greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_word_lengths is called with Ada, Ada Lovelace, and Agent 007
    Then the results are [6, 3], [6, 3, 8], and [6, 5, 3]
    And each result is a plain list of int

  @SCN002
  Scenario: Split on any whitespace without producing empty words
    Given the installed nmg_sdlc_smoke package
    When greeting_word_lengths is called with Ada tab Lee, space Ada space, and Ada two-spaces Lee
    Then the results are [6, 3, 3], [6, 3], and [6, 3, 3]
    And no result contains 0

  @SCN003
  Scenario: Count code points without normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_word_lengths is called with Zo plus U+00EB, Zoe plus U+0308, and Ada plus U+1F600
    Then the results are [6, 3], [6, 4], and [6, 4]

  @SCN004
  Scenario: Agree with the existing word helpers
    Given the installed nmg_sdlc_smoke package
    When greeting_word_lengths is called with Ada, Ada Lovelace, Agent 007, O'Brien, Ada tab Lee, and Zoe plus U+0308
    Then each result equals the lengths of greeting_words of the same name
    And each result has as many values as greeting_word_count of the same name

  @SCN005
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_word_lengths is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN006
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_word_lengths of Ada
    Then it prints [6, 3] and greeting_word_lengths is listed in nmg_sdlc_smoke.__all__
    And the README documents the word-length rule and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
