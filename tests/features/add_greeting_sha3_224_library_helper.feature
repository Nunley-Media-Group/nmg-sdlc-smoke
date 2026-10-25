Feature: Return the SHA3-224 hex digest of the completed greeting

  @SCN001
  Scenario: Return the SHA3-224 hex digest of the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_sha3_224 is called with Ada and Ada Lovelace
    Then the results are the 56-character hex strings 4f8b1b1e2d62e0fc1292bbc88641b8883bcccc2d0087052131c359aa and 196e97d0ffcb84a93f4be2879561b59bdf6970263657fb1c057c8886

  @SCN002
  Scenario: Hash the UTF-8 encoding of non-ASCII greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_sha3_224 is called with Zo plus U+00EB
    Then the result is 04b9e41ed63e300fa54d7a8fa8f1bf97ef6e2ce4a7c9e61ba6565ed3, the hashlib SHA3-224 hex digest of the UTF-8 encoded greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_sha3_224 is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_sha3_224 of Ada
    Then it prints the Ada SHA3-224 digest and greeting_sha3_224 is listed in nmg_sdlc_smoke.__all__
    And the README documents the lowercase hex UTF-8 SHA3-224 result, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
