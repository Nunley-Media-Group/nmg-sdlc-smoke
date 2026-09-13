Feature: Add nmg-smoke quotes flag for nmg-sdlc 379 verification
  As a maintainer running the registered final verification for nmg-sdlc 379
  I want one tiny optional quotes formatting flag in the disposable nmg-smoke CLI
  So that the registered provider can exercise canonical spec publication and normal consumer delivery against one fresh fixture

  @SCN001
  Scenario: Quotes wrap the fully composed greeting
    Given the installed nmg-smoke console script and a valid name
    When nmg-smoke --quotes --uppercase --prefix ok-colon-space --parentheses --braces Ada runs
    Then the process exits 0
    And stdout is exactly double-quote open-brace open-parenthesis ok-colon-space HELLO-comma-space-ADA close-parenthesis close-brace double-quote followed by one newline
    And stderr is empty

  @SCN002
  Scenario: Omitting quotes preserves current output
    Given the installed nmg-smoke console script and a valid name
    When nmg-smoke Ada runs without --quotes
    Then the process exits 0
    And stdout is exactly Hello-comma-space-Ada followed by one newline
    And stderr is empty
