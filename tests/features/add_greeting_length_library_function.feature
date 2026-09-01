# File: tests/features/add_greeting_length_library_function.feature
# Generated from: specs/44-add-greeting-length-library-function/requirements.md
Feature: Add greeting_length library function
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want a greeting_length(name) library function that returns the number of characters in greet(name)
  So that callers can observe greeting size from the existing greeting contract without changing greet or the CLI

  @SCN001
  Scenario: Valid name returns the greeting character count
    Given the library is importable
    When greeting_length is called with Ada
    Then it returns 10
    And that value equals the Python len of greet Ada which is Hello, Ada

  @SCN002
  Scenario: A different valid name returns a matching different count
    Given the library is importable
    When greeting_length is called with Jo
    Then it returns 9
    And that value equals the Python len of greet Jo which is Hello, Jo
    And the result is not hardcoded to the Ada count

  @SCN003
  Scenario: Invalid names raise the existing greet validation error
    Given the library is importable
    When greeting_length is called with a blank, whitespace-only, or non-string name
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
