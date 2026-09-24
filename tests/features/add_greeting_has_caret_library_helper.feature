Feature: Check for a literal caret in a completed greeting
  Library callers can inspect a greeting without changing the existing greeting contract.

  @SCN001
  Scenario: Caret occurs in the completed greeting
    Given a valid name Ada^
    When I ask whether its completed greeting contains a literal caret
    Then the result is True

  @SCN002
  Scenario: Caret does not occur in the completed greeting
    Given a valid name Ada
    When I ask whether its completed greeting contains a literal caret
    Then the result is False

  @SCN003
  Scenario: Invalid names retain greet validation
    Given a blank, whitespace-only, or non-string name
    When I ask whether its completed greeting contains a literal caret
    Then it raises the same ValueError as greet
