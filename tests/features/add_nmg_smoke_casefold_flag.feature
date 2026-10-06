# File: tests/features/add_nmg_smoke_casefold_flag.feature
# Generated from: specs/197-add-nmg-smoke-casefold-flag/requirements.md
Feature: Add nmg-smoke --casefold flag
  As a maintainer running the nmg-smoke console script
  I want a --casefold flag that applies Unicode casefolding to the greeting
  So that I get caseless-comparison output such as hello, strasse from any input casing alongside the existing case and formatting options

  @SCN001
  Scenario: Casefold the greeting
    Given the installed nmg-smoke console script
    When nmg-smoke --casefold Straße runs
    Then the process exits 0
    And stdout is exactly hello-comma-space-strasse followed by one newline
    And stderr is empty

  @SCN002
  Scenario: Uppercase and Greek names use Python str.casefold semantics
    Given the installed nmg-smoke console script
    When nmg-smoke --casefold runs with ADA and with ΣΊΣΥΦΟΣ
    Then every process exits 0
    And the stdouts are exactly hello, ada and hello, σίσυφοσ respectively, each followed by one newline

  @SCN003
  Scenario: Casefold composes with existing formatting options
    Given the installed nmg-smoke console script
    When nmg-smoke --casefold --prefix OK-colon-space --quotes --repeat 2 --no-newline Straße runs
    Then the process exits 0
    And stdout is exactly two double-quoted OK-colon-space hello-comma-space-strasse greetings separated by one newline with no final newline
    And stderr is empty

  @SCN004
  Scenario: Casefold cannot be combined with another case flag
    Given the installed nmg-smoke console script
    When nmg-smoke runs --casefold together with --uppercase, --lowercase, --swapcase, and --titlecase in both argument orders
    Then every process exits 2
    And every stderr contains not allowed with argument
    And every stdout is empty

  @SCN005
  Scenario: Blank name with casefold still fails
    Given the installed nmg-smoke console script
    When nmg-smoke --casefold runs with a single-space name
    Then the process exits 1
    And stderr contains nmg-smoke: error: name must not be blank
    And stdout is empty

  @SCN006
  Scenario: Default and lowercase output and help are preserved
    Given the installed nmg-smoke console script
    When nmg-smoke runs with Ada, with --lowercase Straße, and with --help
    Then every process exits 0
    And the first two stdouts are exactly Hello, Ada and hello, straße, each followed by one newline
    And the help stdout lists --casefold
