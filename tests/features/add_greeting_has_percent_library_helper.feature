Feature: Check for literal percent in a completed greeting
  Library callers can inspect a greeting without changing the greeting contract.

  @SCN001
  Scenario: Percent occurs in the completed greeting
    Given a valid name Ada%
    When I ask whether its completed greeting contains a literal percent sign
    Then the result is True

  @SCN002
  Scenario: Percent does not occur in the completed greeting
    Given a valid name Ada
    When I ask whether its completed greeting contains a literal percent sign
    Then the result is False

  @SCN003
  Scenario Outline: Invalid names retain greet validation
    Given an invalid <kind> name
    When I ask whether its completed greeting contains a literal percent sign
    Then it raises the same ValueError as greet

    Examples:
      | kind            |
      | blank           |
      | whitespace-only |
      | non-string None |
      | non-string int  |
