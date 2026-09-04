# File: tests/features/add_greeting_ends_with_exclamation_library_function.feature
# Generated from: specs/79-add-greeting-ends-with-exclamation-library-function/requirements.md
Feature: Add greeting_ends_with_exclamation library function
  As a maintainer exercising nmg-sdlc against this disposable Python host
  I want a public greeting helper with one trailing exclamation mark
  So that callers can reuse the existing greeting and validation contract

  @SCN001
  Scenario: Append one exclamation mark
    Given the library is importable for the exclamation helper
    When greeting_ends_with_exclamation is called with Ada
    Then it returns exactly Hello, Ada!

  @SCN002
  Scenario: Preserve valid names
    Given a valid name contains leading and trailing spaces
    When greeting_ends_with_exclamation is called with that name
    Then every name character is preserved before the final exclamation mark

  @SCN003
  Scenario: Preserve existing validation
    Given the exclamation helper is imported from the public package
    When greeting_ends_with_exclamation receives invalid names
    Then each exclamation helper call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Preserve existing greeting and CLI behavior
    Given the distribution is installed for exclamation regression coverage
    When greet and nmg-smoke are used with Ada
    Then greet returns Hello, Ada unchanged
    And the CLI exits 0 and prints Hello, Ada followed by one newline
