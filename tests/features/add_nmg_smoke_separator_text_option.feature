# File: tests/features/add_nmg_smoke_separator_text_option.feature
#
# Generated from: specs/98-add-nmg-smoke-separator-text-option/requirements.md
Feature: Add nmg-smoke --separator TEXT option
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want nmg-smoke --separator TEXT to control the text between repeated rendered greetings
  So that a registered smoke queue for nmg-sdlc #374 can observe one minimal new CLI option without changing greeting, prefix, uppercase, name, or error behavior

  @SCN001
  Scenario: Repeat 2 with an explicit separator keeps the final newline
    Given the distribution is installed with its console script
    When nmg-smoke --repeat 2 --separator ' | ' Ada is run
    Then the process exits 0
    And stdout is exactly Hello, Ada | Hello, Ada followed by a single newline
    And stderr is empty

  @SCN002
  Scenario: Omitting --separator preserves current repeated lines
    Given the distribution is installed with its console script
    When nmg-smoke --repeat 2 Ada is run
    Then the process exits 0
    And stdout is exactly two lines of Hello, Ada, each followed by a newline
    And stderr is empty
