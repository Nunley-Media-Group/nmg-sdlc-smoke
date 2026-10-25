Feature: Return the SHA-512 hex digest of the completed greeting

  @SCN001
  Scenario: Return the SHA-512 hex digest of the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_sha512 is called with Ada and Ada Lovelace
    Then the results are the 128-character hex strings 8abfe44c9cccb8990fcecac86c840fce7ccb1949a4eb49569c0f0cedc1481a8cdac6a37dd286d2d1d8175ebd63ff071b8882052d0a0bd874f88e03ad812215e2 and 6c200b8221e61ef4fa3e4028a8484253f8abf94b0034d52be2224f37d7039c7b081304d248d8b6424c7455c1dac951ddd61968721ef9969f43fb36ea87abbb53

  @SCN002
  Scenario: Hash the UTF-8 encoding of non-ASCII greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_sha512 is called with Zo plus U+00EB
    Then the result is f93e61e8fa95d7f3f732ba7cd41ab19b7b2bbee43b20e1f1aca2c7ffeac6d39444bbaec839b5cd2e7e5dbc5adb4c651d3c65fa1fb3765fd5cde55509fe5b2e59, the hashlib SHA-512 hex digest of the UTF-8 encoded greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_sha512 is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_sha512 of Ada
    Then it prints the Ada SHA-512 digest and greeting_sha512 is listed in nmg_sdlc_smoke.__all__
    And the README documents the lowercase hex UTF-8 SHA-512 result, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
