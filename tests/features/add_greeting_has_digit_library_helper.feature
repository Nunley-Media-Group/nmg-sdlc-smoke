Feature: Detect decimal digits in a completed greeting
  Scenario: Detect ASCII and Unicode decimal digits
    Given the installed greeting library with a digit helper
    When I check Ada7, Ada٣, and Ada for decimal digits
    Then the results are True, True, and False

  Scenario: Reject invalid names with existing validation
    Given blank, whitespace-only, and non-string digit-helper inputs
    When I check each invalid name for decimal digits
    Then each raises the existing greet ValueError

  Scenario: Preserve existing greeting and CLI output
    Given the installed package with its existing public exports
    When greet and nmg-smoke greet Ada
    Then both return the existing Hello, Ada output with the CLI newline
    And all existing public exports remain available
