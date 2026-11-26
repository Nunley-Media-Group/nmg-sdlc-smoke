Feature: Count ASCII characters in the completed greeting

  @SCN001
  Scenario: Count ASCII characters in a plain greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_ascii_count is called with Ada, Zo U+00EB, and U+674E U+96F7
    Then the results are 10, then 9, then 7
    And each result is an int

  @SCN002
  Scenario: Count code points without normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_ascii_count is called with Zoe U+0308 and Ada space U+1F600
    Then the results are 10, then 11
    And each result equals the number of code points at or below 127 in greet of the same name
    And each result plus greeting_non_ascii_count of the same name equals the greeting length

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_ascii_count is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints greeting_ascii_count of Zo U+00EB
    Then it prints 9 and greeting_ascii_count is listed in nmg_sdlc_smoke.__all__
    And the README documents the code-point counting rule and the inherited invalid-name error
