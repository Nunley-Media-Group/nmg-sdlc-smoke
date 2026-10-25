Feature: Return the MD5 hex digest of the completed greeting

  @SCN001
  Scenario: Return the MD5 hex digest of the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_md5 is called with Ada and Ada Lovelace
    Then the results are the hex strings a4f502ca98cce831af61b0fe0a319382 and bd0b2e5ea5baf6775e93262ce37d5a4a

  @SCN002
  Scenario: Hash the UTF-8 encoding of non-ASCII greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_md5 is called with Zo plus U+00EB
    Then the result is 26ed66c6559b1e033c70ef2301fe0beb, the hashlib MD5 hex digest of the UTF-8 encoded greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_md5 is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_md5 of Ada
    Then it prints a4f502ca98cce831af61b0fe0a319382 and greeting_md5 is listed in nmg_sdlc_smoke.__all__
    And the README documents the lowercase hex UTF-8 MD5 result, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
