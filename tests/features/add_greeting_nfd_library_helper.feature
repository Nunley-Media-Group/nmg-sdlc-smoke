Feature: Return the completed greeting in Unicode NFD

  @SCN001
  Scenario: Decompose precomposed characters
    Given the installed nmg_sdlc_smoke package
    When greeting_nfd is called with precomposed Chloé and precomposed Ångström
    Then the results are Hello, Chloe plus U+0301 with 13 code points, then Hello, A plus U+030A ngstro plus U+0308 m with 17 code points
    And each result is a str

  @SCN002
  Scenario: Leave text without decomposable characters unchanged
    Given the installed nmg_sdlc_smoke package
    When greeting_nfd is called with Ada, Ada Lovelace, and Chloe plus U+0301
    Then each result equals greet of the same name

  @SCN003
  Scenario: Apply canonical, not compatibility, normalization
    Given the installed nmg_sdlc_smoke package
    When greeting_nfd is called with U+FB01 ona and Ada two-spaces Lovelace
    Then the results are Hello, U+FB01 ona with 11 code points, then Hello, Ada two-spaces Lovelace

  @SCN004
  Scenario: Agree with unicodedata NFD
    Given the installed nmg_sdlc_smoke package
    When greeting_nfd is called with Ada, precomposed Chloé, U+FB01 ona, and O'Brien-Smith
    Then each result equals unicodedata NFD normalization of greet of the same name
    And each result is NFD-normalized

  @SCN005
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_nfd is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN006
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints the length of greeting_nfd of precomposed Chloé
    Then it prints 13 and greeting_nfd is listed in nmg_sdlc_smoke.__all__
    And the README documents the NFD rule and the inherited invalid-name error
