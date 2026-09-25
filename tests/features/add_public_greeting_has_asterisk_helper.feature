Feature: Detect a literal ASCII asterisk in a completed greeting

  @SCN001
  Scenario: ASCII asterisk occurs in the completed greeting
    Given the public greeting library and valid name Ada followed by ASCII U+002A
    When greeting_has_asterisk is called with Ada followed by ASCII U+002A
    Then the completed greeting is Hello, Ada followed by ASCII U+002A and the result is Python True

  @SCN002
  Scenario: Missing ASCII asterisk does not match
    Given the public greeting library and valid name Ada without an asterisk
    When greeting_has_asterisk is called with Ada
    Then the completed greeting is Hello, Ada and the asterisk result is Python False

  @SCN003
  Scenario: U+2217 asterisk operator does not match
    Given the public greeting library and valid name Ada followed by U+2217
    When greeting_has_asterisk is called with Ada followed by U+2217
    Then the completed greeting is Hello, Ada followed by U+2217 and the result is Python False

  @SCN004
  Scenario: Invalid names retain greet validation
    Given invalid names empty, whitespace-only, None, and 42 for the asterisk helper
    When greeting_has_asterisk is called with each invalid name
    Then each asterisk helper call raises ValueError with message name must not be blank

  @SCN005
  Scenario: The public helper, greeting, and CLI remain available
    Given the public greeting library and installed nmg-smoke script for the asterisk helper
    When greeting_has_asterisk is imported, greet Ada is evaluated, and nmg-smoke Ada is run
    Then the import succeeds, the library returns Hello, Ada, and the CLI exits zero with one Hello, Ada newline on stdout and empty stderr
