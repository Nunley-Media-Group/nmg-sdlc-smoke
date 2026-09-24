Feature: Detect a literal equals sign in a completed greeting

  @SCN001
  Scenario: ASCII equals occurs in the completed greeting
    Given the valid name Ada= and the public greeting library
    When greeting_has_equal is called with that name
    Then the completed greeting is Hello, Ada= and the result is True

  @SCN002
  Scenario: ASCII equals is absent from completed greetings
    Given valid names Ada and Ada＝ and the public greeting library
    When greeting_has_equal is called with each name
    Then each completed greeting lacks ASCII equals and each result is False

  @SCN003
  Scenario: Invalid names retain greet validation
    Given invalid names empty, whitespace-only, None, and 42
    When greeting_has_equal is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Existing public greeting interfaces remain intact
    Given the previously public package exports and the installed nmg-smoke script
    When those exports and greeting_has_equal are imported and greet Ada, greeting_has_hash Ada#, and nmg-smoke Ada are invoked
    Then all imports succeed, the library returns Hello, Ada and True, and the CLI exits zero with one Hello, Ada newline on stdout and empty stderr
