Feature: Return the initials of the completed greeting's words

  @SCN001
  Scenario: Return initials for single-word names
    Given the installed nmg_sdlc_smoke package
    When greeting_initials is called with Ada and Zo plus U+00EB
    Then the results are the strings HA and HZ

  @SCN002
  Scenario: Handle multi-word names, whitespace runs, and preserve case
    Given the installed nmg_sdlc_smoke package
    When greeting_initials is called with Ada Lovelace, Ada space-tab-space Lovelace, and ada lovelace
    Then the results are HAL, HAL, and Hal
    And each result length equals greeting_word_count of the same name

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_initials is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_initials of Ada
    Then it prints HA and greeting_initials is listed in nmg_sdlc_smoke.__all__
    And the README documents the case-preserving initials of the complete greeting and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
