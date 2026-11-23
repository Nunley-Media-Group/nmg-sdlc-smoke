Feature: Return the title-cased completed greeting

  @SCN001
  Scenario: Title-case single- and multi-word names
    Given the installed nmg_sdlc_smoke package
    When greeting_titlecase is called with ada, ADA LOVELACE, and ada lovelace
    Then the results are Hello, Ada, then Hello, Ada Lovelace, then Hello, Ada Lovelace
    And each result is a str

  @SCN002
  Scenario: Follow str.title() rules for apostrophes, digits, and non-ASCII letters
    Given the installed nmg_sdlc_smoke package
    When greeting_titlecase is called with o'brien, agent 007x, and åsa
    Then the results are Hello, O'Brien, then Hello, Agent 007X, then Hello, Åsa

  @SCN003
  Scenario: Agree with greet and the CLI flag
    Given the installed nmg_sdlc_smoke package
    When greeting_titlecase is called with ada, ADA LOVELACE, o'brien, and Ada tab Lovelace
    Then each result equals str.title() of greet of the same name
    And nmg-smoke --titlecase ada prints the greeting_titlecase result for ada followed by one newline

  @SCN004
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_titlecase is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN005
  Scenario: Expose and document the helper
    Given the README Library section
    When the README Library example runs and prints greeting_titlecase of ada lovelace
    Then it prints Hello, Ada Lovelace and greeting_titlecase is listed in nmg_sdlc_smoke.__all__
    And the README documents the str.title() rule and the inherited invalid-name error
