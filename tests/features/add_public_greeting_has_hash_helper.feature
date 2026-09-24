Feature: Detect a literal hash in a completed greeting
  Library callers can query hash presence without changing existing greeting behavior.

  @SCN001
  Scenario: Hash occurs in the completed greeting
    Given the valid name Ada# and the public greeting library
    When greeting_has_hash is called with that name
    Then the completed greeting is Hello, Ada# and the result is True

  @SCN002
  Scenario: Hash does not occur in the completed greeting
    Given the valid name Ada and the public greeting library
    When greeting_has_hash is called with that name
    Then the completed greeting is Hello, Ada and the result is False

  @SCN003
  Scenario: Invalid names retain greet validation
    Given the invalid names empty, whitespace-only, None, and 42
    When greeting_has_hash is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Existing greeting interfaces remain intact
    Given the public greeting helpers and the installed nmg-smoke console script
    When greet Ada, greeting_has_question_mark Ada?, and nmg-smoke Ada are invoked
    Then they yield Hello, Ada, True, and one Hello, Ada newline on stdout with exit zero
