Feature: Detect a literal plus in a completed greeting
  Library callers can query plus presence without changing existing greeting behavior.

  @SCN001
  Scenario: Plus occurs in the completed greeting
    Given the valid name Ada+ and the public greeting library
    When greeting_has_plus is called with that name
    Then the completed greeting is Hello, Ada+ and the result is True

  @SCN002
  Scenario: Plus does not occur in the completed greeting
    Given the valid name Ada and the public greeting library
    When greeting_has_plus is called with that name
    Then the completed greeting is Hello, Ada and the result is False

  @SCN003
  Scenario: Invalid names retain greet validation
    Given the invalid names empty, whitespace-only, None, and 42
    When greeting_has_plus is called with each invalid name
    Then each call raises ValueError with message name must not be blank
