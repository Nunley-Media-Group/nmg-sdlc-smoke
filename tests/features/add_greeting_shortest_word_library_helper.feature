Feature: Return the shortest word of the completed greeting

  @SCN001
  Scenario: Return the shortest word for simple and multi-word greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_shortest_word is called with Ada, Ada Lovelace, and Agent 007
    Then the results are Ada, then Ada, then 007
    And each result is a plain str

  @SCN002
  Scenario: Return the first word on a length tie
    Given the installed nmg_sdlc_smoke package
    When greeting_shortest_word is called with Bertha and with Bo Al
    Then the results are Hello, then Bo

  @SCN003
  Scenario: Return the greeting word when every name word is longer
    Given the installed nmg_sdlc_smoke package
    When greeting_shortest_word is called with Lovelace
    Then the result is Hello,

  @SCN004
  Scenario: Split on any whitespace
    Given the installed nmg_sdlc_smoke package
    When greeting_shortest_word is called with Ada tab Lovelace, space Ada space, and Bo two-spaces Al
    Then the results are Ada, then Ada, then Bo

  @SCN005
  Scenario: Measure code points without normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_shortest_word is called with Chlo plus U+00E9, and Chloe plus U+0301
    Then the results are the unchanged precomposed name and Hello,

  @SCN006
  Scenario: Agree with the existing word helpers
    Given the installed nmg_sdlc_smoke package
    When greeting_shortest_word is called with Ada, Ada Lovelace, Agent 007, Bertha, Bo Al, O'Brien-Smith, and Chloe plus U+0301
    Then each result is one of greeting_words of the same name
    And each result is as long as the minimum of greeting_word_lengths of the same name

  @SCN007
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_shortest_word is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN008
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_shortest_word of Ada
    Then it prints Ada and greeting_shortest_word is listed in nmg_sdlc_smoke.__all__
    And the README documents the shortest-word rule and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
