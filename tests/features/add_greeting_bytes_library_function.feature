# File: tests/features/add_greeting_bytes_library_function.feature
# Generated from: specs/53-add-greeting-bytes-library-function/requirements.md
Feature: Add greeting_bytes library function
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want a greeting_bytes(name) library function that returns the UTF-8 byte length of greet(name)
  So that callers can observe greeting size in bytes from the existing greeting contract without changing greet or the CLI

  @SCN001
  Scenario: Valid ASCII name returns the greeting UTF-8 byte count
    Given the library is importable
    When greeting_bytes is called with Ada
    Then it returns 10
    And that value equals the UTF-8 byte length of greet Ada which is Hello, Ada

  @SCN002
  Scenario: A non-ASCII name returns UTF-8 bytes, not character count
    Given the library is importable
    When greeting_bytes is called with É
    Then it returns 9
    And that value equals the UTF-8 byte length of greet É which is Hello, É
    And that value is not equal to greeting_length of É which is 8
    And the result is not hardcoded to the Ada count

  @SCN003
  Scenario: Invalid names raise the existing greet validation error
    Given the library is importable
    When greeting_bytes is called with a blank, whitespace-only, or non-string name
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
