Feature: Detect a semicolon in a completed greeting

  @SCN001
  Scenario: Detect literal semicolon
    Given the installed greeting library and a valid name containing a semicolon
    When greeting_has_semicolon is called with Ada;
    Then it returns True for the completed greeting Hello, Ada;

  @SCN002
  Scenario: Report no semicolon
    Given the installed greeting library and a valid name without a semicolon
    When greeting_has_semicolon is called with Ada
    Then it returns False for the completed greeting Hello, Ada

  @SCN003
  Scenario: Reject invalid names
    Given empty, whitespace-only, and non-string names
    When greeting_has_semicolon is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Preserve public helpers and default CLI output
    Given the installed package and its console script
    When greet and nmg-smoke greet Ada
    Then the library returns Hello, Ada and the CLI exits 0 with exactly Hello, Ada and one newline on stdout and empty stderr
    And all previously exported public helpers remain importable
