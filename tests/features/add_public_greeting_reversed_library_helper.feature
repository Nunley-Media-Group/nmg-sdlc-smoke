Feature: Reverse the complete greeting by code point

  @SCN001
  Scenario: Reverse the complete greeting by code point
    Given the installed nmg_sdlc_smoke package
    When greeting_reversed is called with Ada and with Zoë spelled with the precomposed U+00EB code point
    Then the results are exactly adA ,olleH and ëoZ ,olleH

  @SCN002
  Scenario: Reject invalid names with the existing validation
    Given the invalid names empty, three spaces, and None
    When greeting_reversed is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN003
  Scenario: Export the helper without changing existing surfaces
    Given the installed nmg_sdlc_smoke package
    When greeting_reversed is imported from nmg_sdlc_smoke, greet is called with Ada, and nmg-smoke Ada runs
    Then greeting_reversed is listed in __all__ alongside every previously listed export
    And greet returns Hello, Ada and nmg-smoke prints Hello, Ada with one newline and exit status 0
