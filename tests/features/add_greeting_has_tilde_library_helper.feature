Feature: Detect a literal tilde in a completed greeting

  @SCN001
  Scenario: Detect a literal tilde
    Given the installed greeting library and a valid name containing a tilde
    When greeting_has_tilde is called with Ada~
    Then it returns True for the completed greeting Hello, Ada~

  @SCN002
  Scenario: Report no tilde
    Given the installed greeting library and a valid name without a tilde
    When greeting_has_tilde is called with Ada
    Then it returns False for the completed greeting Hello, Ada

  @SCN003
  Scenario: Reject invalid names
    Given empty, whitespace-only, and non-string names
    When greeting_has_tilde is called with each invalid name
    Then each call raises ValueError with message name must not be blank
