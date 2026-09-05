Feature: Add LIVE_SMOKE_362_A verification marker
  A fresh deterministic marker exercises the complete delivery lifecycle.

  @SCN001
  Scenario: Marker has exact content
    Given the repository root for issue 82
    When LIVE_SMOKE_362_A.txt is read
    Then it contains exactly LIVE_SMOKE_362_A followed by one newline
