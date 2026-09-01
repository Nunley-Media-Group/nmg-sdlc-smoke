# File: tests/features/add_greeting_is_ascii_library_function.feature
# Generated from: specs/57-add-greeting-is-ascii-library-function/requirements.md
Feature: Add greeting_is_ascii library function
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want a greeting_is_ascii(name) library function that returns whether greet(name) is ASCII
  So that callers can observe ASCII-ness of the existing greeting contract without changing greet or the CLI

  @SCN001
  Scenario: Valid ASCII name returns True
    Given the library is importable
    When greeting_is_ascii is called with Ada
    Then it returns True
    And that value equals greet Ada isascii which is Hello, Ada

  @SCN002
  Scenario: Valid non-ASCII name returns False
    Given the library is importable
    When greeting_is_ascii is called with É
    Then it returns False
    And that value equals greet É isascii which is Hello, É
    And the result is not hardcoded to the Ada result

  @SCN003
  Scenario: Invalid names raise the existing greet validation error
    Given the library is importable
    When greeting_is_ascii is called with a blank, whitespace-only, or non-string name
    Then it raises ValueError with message name must not be blank
    And that error is the existing greet validation error, not a wrapped or renamed error

  @SCN004
  Scenario: Existing greet and CLI behavior is unchanged
    Given the distribution is installed
    When greet is called with Ada
    Then it returns Hello, Ada
    When nmg-smoke Ada is run
    Then the process exits 0 and prints Hello, Ada followed by a single newline
    And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting
