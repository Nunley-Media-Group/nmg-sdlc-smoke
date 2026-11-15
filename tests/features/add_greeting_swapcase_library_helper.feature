Feature: Return the completed greeting with its letter case swapped

  @SCN001
  Scenario: Return the swap-cased greeting for valid names
    Given the installed nmg_sdlc_smoke package
    When greeting_swapcase is called with Ada, Zo plus U+00EB, and O'Neil 42
    Then the results are hELLO, aDA and hELLO, zO plus U+00CB and hELLO, o'nEIL 42
    And each result equals the swapcase of the greeting

  @SCN002
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_swapcase is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN003
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_swapcase of Ada
    Then it prints hELLO, aDA and greeting_swapcase is listed in nmg_sdlc_smoke.__all__
    And the README documents the case swap of the complete greeting and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
