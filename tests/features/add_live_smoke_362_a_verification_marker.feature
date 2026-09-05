Feature: Add LIVE_SMOKE_362_A verification marker
  A fresh deterministic marker exercises the complete delivery lifecycle.

  @SCN001
  Scenario: Marker has exact content
    Given the repository root for issue 82
    When LIVE_SMOKE_362_A.txt is read
    Then it contains exactly LIVE_SMOKE_362_A followed by one newline

  @SCN002
  Scenario: Existing verification remains green
    Given the issue 82 marker exists
    When pytest, feature pytest, and Ruff run for issue 82
    Then each issue 82 verification command exits zero

  @SCN003
  Scenario: Product change is isolated
    Given the completed issue 82
    When changed product paths for issue 82 are inspected
    Then only LIVE_SMOKE_362_A.txt is added as an issue 82 product change
