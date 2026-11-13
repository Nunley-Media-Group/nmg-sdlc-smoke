Feature: Return the SHAKE-256 hex digest of the completed greeting

  @SCN001
  Scenario: Return the 64-byte SHAKE-256 hex digest of the greeting
    Given the installed nmg_sdlc_smoke package
    When greeting_shake_256 is called with Ada and Zo plus U+00EB
    Then the results are 51412b094871bbe3e276da7fa1fad8bd4bfae7cfbeb88db9e732d1f32461e67c41e270771c528e629790ba47af4772e92632de0b5b8f63cf801ef7eb8d6a29a7 and f1548a17e00c5729deeb887a4c5906e0dcdd3ef62f2e0b3a27a34dd94ef06c9a439d43b9dc7f31c5a71c17ea7ee5a946a4e32d2ed0981916c59d5d8a10ece632
    And each result is 128 lowercase hexadecimal characters equal to the 64-byte SHAKE-256 hex digest of the UTF-8 greeting

  @SCN002
  Scenario: Preserve invalid-name behavior
    Given the invalid names empty, space-tab, None, and 42
    When greeting_shake_256 is called with each invalid name
    Then each call raises ValueError with message name must not be blank

  @SCN003
  Scenario: Expose and document the helper without changing the CLI
    Given the README Library section
    When the README Library example runs and prints greeting_shake_256 of Ada
    Then it prints 51412b094871bbe3e276da7fa1fad8bd4bfae7cfbeb88db9e732d1f32461e67c41e270771c528e629790ba47af4772e92632de0b5b8f63cf801ef7eb8d6a29a7 and greeting_shake_256 is listed in nmg_sdlc_smoke.__all__
    And the README documents the fixed 64-byte SHAKE-256 hex output over the UTF-8 greeting and the inherited invalid-name error
    And nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0
