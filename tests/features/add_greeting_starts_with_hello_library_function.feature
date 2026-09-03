# File: tests/features/add_greeting_starts_with_hello_library_function.feature
# Generated from: specs/68-add-greeting-starts-with-hello-library-function/requirements.md
Feature: Add greeting_starts_with_hello library function
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want a greeting_starts_with_hello(name) library function that returns whether greet(name) starts with Hello, 
  So that callers can observe that prefix from the existing greeting contract without changing greet or the CLI

  @SCN001
  Scenario: Valid name returns True
    Given the library is importable
    When greeting_starts_with_hello is called with Ada
    Then it returns True
    And that value equals greet Ada startswith Hello comma space which is Hello, Ada
    And the return value is the Python bool True, not the string True

  @SCN002
  Scenario: A different valid name also returns True from the prefix check
    Given the library is importable
    When greeting_starts_with_hello is called with Jo
    Then it returns True
    And that value equals greet Jo startswith Hello comma space which is Hello, Jo
    And the result is not hardcoded to the Ada call only

  @SCN003
  Scenario: Invalid names raise the existing greet validation error
    Given the library is importable
    When greeting_starts_with_hello is called with a blank, whitespace-only, or non-string name
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
