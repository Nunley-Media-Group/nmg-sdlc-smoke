# File: tests/features/add_nmg_smoke_lowercase_flag.feature
# Generated from: specs/188-add-nmg-smoke-lowercase-flag/requirements.md
Feature: Add nmg-smoke --lowercase flag
  As a maintainer running the nmg-smoke console script
  I want a --lowercase flag that lowercases the greeting
  So that I can get hello, ada output alongside the existing formatting options

  @SCN001
  Scenario: Lowercase the greeting
    Given the installed nmg-smoke console script
    When nmg-smoke --lowercase Ada runs
    Then the process exits 0
    And stdout is exactly hello-comma-space-ada followed by one newline
    And stderr is empty

  @SCN002
  Scenario: Lowercase composes with existing formatting options
    Given the installed nmg-smoke console script
    When nmg-smoke --lowercase --prefix OK-colon-space --parentheses --repeat 2 --no-newline ADA runs
    Then the process exits 0
    And stdout is exactly two parenthesized OK-colon-space hello-comma-space-ada greetings separated by one newline with no final newline
    And stderr is empty

  @SCN003
  Scenario: Non-ASCII names use Python str.lower semantics
    Given the installed nmg-smoke console script
    When nmg-smoke --lowercase runs with ÅSA and with Straße
    Then every process exits 0
    And the stdouts are exactly hello, åsa and hello, straße respectively, each followed by one newline

  @SCN004
  Scenario: Uppercase and lowercase cannot be combined
    Given the installed nmg-smoke console script
    When nmg-smoke runs with --uppercase --lowercase Ada and with --lowercase --uppercase Ada
    Then every process exits 2
    And every stderr contains not allowed with argument
    And every stdout is empty

  @SCN005
  Scenario: Blank name with lowercase still fails
    Given the installed nmg-smoke console script
    When nmg-smoke --lowercase runs with a single-space name
    Then the process exits 1
    And stderr contains nmg-smoke: error: name must not be blank
    And stdout is empty

  @SCN006
  Scenario: Default output, uppercase output, and help are preserved
    Given the installed nmg-smoke console script
    When nmg-smoke runs with Ada, with --uppercase Ada, and with --help
    Then every process exits 0
    And the first two stdouts are exactly Hello, Ada and HELLO, ADA, each followed by one newline
    And the help stdout lists --lowercase
