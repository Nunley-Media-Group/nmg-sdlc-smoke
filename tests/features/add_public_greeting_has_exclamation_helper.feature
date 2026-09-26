Feature: Detect a literal exclamation mark in a completed greeting

  @SCN001
  Scenario: Detect literal exclamation in a completed greeting
    Given the installed public greeting package and valid name Ada!
    When greeting_has_exclamation is called with Ada!
    Then greet returns Hello, Ada! and the helper returns True

  @SCN002
  Scenario: Reject absent and fullwidth exclamation
    Given valid names Ada and Ada！
    When greeting_has_exclamation is called with each valid name
    Then each completed greeting lacks literal ! and each helper result is False

  @SCN003
  Scenario: Preserve greet validation for invalid names
    Given invalid names empty, whitespace-only, None, and 42
    When greeting_has_exclamation is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Import and run the documented helper examples
    Given the installed public package and README Library examples Ada! and Ada
    When greeting_has_exclamation is imported from nmg_sdlc_smoke and called with those names
    Then the imported helper returns True and False respectively
