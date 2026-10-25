Feature: Return the SHA3-384 hex digest of the completed greeting

  @SCN001
  Scenario: Return the SHA3-384 hex digest of the completed greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_sha3_384 is called with Ada and Ada Lovelace
    Then the results are the 96-character hex strings 1a0e27fabec84a7b6ff60b8feb3cb3a8f6c3838c4242005c74f61de0149c524ac44e5f4d417d35726285bd9ee10b470b and 251c47136f46312b1918981ecc29cb66876fb6a8023afeb6bd76cee86d3fb37ec6038e70ea082e727343a1e97fb020ea

  @SCN002
  Scenario: Hash the UTF-8 encoding of non-ASCII greetings
    Given the installed nmg_sdlc_smoke package
    When greeting_sha3_384 is called with Zo plus U+00EB
    Then the result is 191915c174eb9ed3dc8f2f91aeebb7c9da27d307f70004046dbd659dbb482cd4c413750218633f933f2224976b4f2311, the hashlib SHA3-384 hex digest of the UTF-8 encoded greeting

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_sha3_384 is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_sha3_384 of Ada
    Then it prints the Ada SHA3-384 digest and greeting_sha3_384 is listed in nmg_sdlc_smoke.__all__
    And the README documents the lowercase hex UTF-8 SHA3-384 result, completed-greeting scope, and inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
