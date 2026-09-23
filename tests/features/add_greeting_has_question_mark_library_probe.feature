Feature: Detect a question mark in a completed greeting

  @AC1
  Scenario: Find a question mark in a valid name
    Given a valid name containing a question mark
    When I call the exported greeting_has_question_mark helper
    Then the result is true

  @AC2
  Scenario: Reject absence of a question mark
    Given a valid name without a question mark
    When I call the exported greeting_has_question_mark helper
    Then the result is false

  @AC3
  Scenario: Preserve existing greeting validation
    Given a blank, whitespace-only, or non-string name
    When I call the exported greeting_has_question_mark helper with each invalid name
    Then the existing greet ValueError is raised
