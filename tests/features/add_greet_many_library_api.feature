# File: tests/features/add_greet_many_library_api.feature
# Generated from: specs/40-add-greet-many-library-api/requirements.md
Feature: Add greet_many library API
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want a greet_many(names) library API that applies the existing greet contract to each name in an iterable
  So that batch greetings are observable in input order without changing greet or the CLI

  @SCN001
  Scenario: Multiple valid names in input order
    Given the library is importable
    When greet_many is called with an iterable of valid names such as Ada and Bob
    Then it returns Hello, Ada and Hello, Bob
    And each element is the result of applying the existing greet contract to the corresponding input name
    And duplicate names produce duplicate greetings in the same positions

  @SCN002
  Scenario: Empty iterable
    Given the library is importable
    When greet_many is called with an empty iterable
    Then it returns an empty list

  @SCN003
  Scenario: First invalid name propagates greet's error
    Given the library is importable
    When greet_many is called with an iterable whose first invalid name is blank, whitespace-only, or non-string
    Then it raises ValueError with message name must not be blank
    And that error is the existing greet validation error, not a wrapped or renamed error
    And it does not return greetings for later names

  @SCN004
  Scenario: Bare string names argument is rejected
    Given the library is importable
    When greet_many is called with a str as the names argument
    Then it raises TypeError
    And it does not iterate the string as characters and does not return per-character greetings

  @SCN005
  Scenario: Existing greet and CLI behavior is unchanged
    Given the distribution is installed
    When greet is called with Ada
    Then it returns Hello, Ada
    When nmg-smoke Ada is run
    Then the process exits 0 and prints Hello, Ada followed by a single newline
    And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting
