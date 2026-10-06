# File: tests/features/add_nmg_smoke_titlecase_flag.feature
# Generated from: specs/194-add-nmg-smoke-titlecase-flag/requirements.md
Feature: Add nmg-smoke --titlecase flag
  As a maintainer running the nmg-smoke console script
  I want a --titlecase flag that title-cases the greeting
  So that I can get Hello, Ada Lovelace output from any input casing alongside the existing case and formatting options

  @SCN001
  Scenario: Title-case the greeting
    Given the installed nmg-smoke console script
    When nmg-smoke --titlecase ada runs
    Then the process exits 0
    And stdout is exactly Hello-comma-space-Ada followed by one newline
    And stderr is empty

  @SCN002
  Scenario: Multi-word, uppercase, punctuated, and non-ASCII names use Python str.title semantics
    Given the installed nmg-smoke console script
    When nmg-smoke --titlecase runs with ADA LOVELACE, with o'neil, and with åsa
    Then every process exits 0
    And the stdouts are exactly Hello, Ada Lovelace and Hello, O'Neil and Hello, Åsa respectively, each followed by one newline

  @SCN003
  Scenario: Titlecase composes with existing formatting options
    Given the installed nmg-smoke console script
    When nmg-smoke --titlecase --prefix ok-colon-space --quotes --repeat 2 --no-newline ADA runs
    Then the process exits 0
    And stdout is exactly two double-quoted ok-colon-space Hello-comma-space-Ada greetings separated by one newline with no final newline
    And stderr is empty

  @SCN004
  Scenario: Titlecase cannot be combined with another case flag
    Given the installed nmg-smoke console script
    When nmg-smoke runs --titlecase together with --uppercase, --lowercase, and --swapcase in both argument orders
    Then every process exits 2
    And every stderr contains not allowed with argument
    And every stdout is empty

  @SCN005
  Scenario: Blank name with titlecase still fails
    Given the installed nmg-smoke console script
    When nmg-smoke --titlecase runs with a single-space name
    Then the process exits 1
    And stderr contains nmg-smoke: error: name must not be blank
    And stdout is empty

  @SCN006
  Scenario: Default, uppercase, lowercase, and swapcase output and help are preserved
    Given the installed nmg-smoke console script
    When nmg-smoke runs with Ada, with --uppercase Ada, with --lowercase Ada, with --swapcase Ada, and with --help
    Then every process exits 0
    And the first four stdouts are exactly Hello, Ada and HELLO, ADA and hello, ada and hELLO, aDA, each followed by one newline
    And the help stdout lists --titlecase
