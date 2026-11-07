Feature: Return the Ascii85 encoding of the completed greeting

  @SCN001
  Scenario: Return the Ascii85 encoding of the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_ascii85 is called with Ada and Ada Lovelace
    Then the results are the Ascii85 strings 87cURD_*"sA75 and 87cURD_*"sA76TSDg#].@:Nj

  @SCN002
  Scenario: Encode the UTF-8 bytes of non-ASCII greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_ascii85 is called with Zo plus U+00EB
    Then the result is 87cURD_*#7Do8U, the base64 module Ascii85 encoding of the UTF-8 encoded greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_ascii85 is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_ascii85 of Ada
    Then it prints 87cURD_*"sA75 and greeting_ascii85 is listed in nmg_sdlc_smoke.__all__
    And the README documents the undelimited, unfolded, unwrapped Ascii85 UTF-8 result, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
