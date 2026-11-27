Feature: Count alphanumeric characters in the completed greeting

  @SCN001
  Scenario: Count alphanumeric characters in a greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_alnum_count is called with Ada, Zo U+00EB, U+674E U+96F7, and R2-D2
    Then the results are 8, then 8, then 7, then 9
    And each result is an int

  @SCN002
  Scenario: Count Unicode digits, exclude marks and emoji, no normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_alnum_count is called with Zoe U+0308, Ada space U+1F600, and Agent space U+0663
    Then the results are 8, then 8, then 11
    And each result equals the number of isalnum code points in greet of the same name

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_alnum_count is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints greeting_alnum_count of R2-D2
    Then it prints 9 and greeting_alnum_count is listed in nmg_sdlc_smoke.__all__
    And the README documents the isalnum counting rule and the inherited invalid-name error
