Feature: Greeting word-count lifecycle fixture
  Scenario Outline: Count words in the greeting
    Given the name "<name>"
    When I call the exported greeting_word_count helper
    Then the word count is <count>

    Examples:
      | name         | count |
      | Ada          | 2     |
      | Ada Lovelace | 3     |

  Scenario: Preserve greeting validation and existing output
    Given blank, whitespace-only, or non-string input
    When I call greeting_word_count for invalid input
    Then it raises the existing greet ValueError
    And existing greeting and CLI contracts remain unchanged

  Scenario: Independently exercise the documented public helper
    Given the documented public helper example
    When I execute the README library example
    Then the documented word counts are reproducible
