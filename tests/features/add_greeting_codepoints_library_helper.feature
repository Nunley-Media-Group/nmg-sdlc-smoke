Feature: Return the Unicode code points of the completed greeting

  @SCN001
  Scenario: Return the greeting's code points for valid names
    Given the installed nmg_sdlc_smoke package
    When greeting_codepoints is called with Ada and Zo plus U+00EB
    Then the results are 72 101 108 108 111 44 32 65 100 97 and 72 101 108 108 111 44 32 90 111 235
    And each result is a list of the ord values of the greeting

  @SCN002
  Scenario: Return one code point per non-BMP character
    Given the installed nmg_sdlc_smoke package
    When greeting_codepoints is called with U+1F600
    Then the result is 72 101 108 108 111 44 32 128512
    And the result length equals greeting_length of U+1F600

  @SCN003
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_codepoints is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN004
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_codepoints of Ada
    Then it prints the list 72 101 108 108 111 44 32 65 100 97 and greeting_codepoints is listed in nmg_sdlc_smoke.__all__
    And the README documents the code-point list of the complete greeting and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
