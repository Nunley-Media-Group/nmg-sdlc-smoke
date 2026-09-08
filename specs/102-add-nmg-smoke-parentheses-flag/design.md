# Design: Add nmg-smoke parentheses flag

**Issue**: #102
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

---

## Overview

Implement the opt-in CLI wrapper specified in requirements.md in the existing thin argparse adapter. Keep the pure greeting library unchanged. No new runtime dependency or helper layer is needed.

## Architecture

### Data Flow

1. Parse the existing arguments plus long-only boolean --parentheses using store_true.
2. Obtain the greeting through the existing validation path.
3. Apply existing uppercase, then prepend the prefix literally.
4. Only when enabled, compose one literal opening parenthesis, the complete message, and one literal closing parenthesis.
5. Reuse the existing repeat loop and final-newline selection without alteration.

## API / Interface Changes

| Interface | Input | Output |
|-----------|-------|--------|
| nmg-smoke | --parentheses, no value, default false | Each fully composed successful greeting enclosed in literal parentheses |

No short alias. Existing library signatures, errors, positional-name requirement, and other option semantics stay unchanged. Parentheses already present in content are not escaped, stripped, or normalized; the wrapper adds only its two literal characters. Prefix text remains outside uppercase conversion but inside the wrapper. Internal newlines remain untouched; wrapping applies to the message, not separately to physical lines.

## Database / Storage Changes

None.

## State Management

Only the invocation-local argparse boolean is added. No persistent state.

## UI Components

No graphical UI. The CLI help exposes the new flag through argparse.

## Alternatives Considered

| Option | Decision |
|--------|----------|
| Wrap the full repeated stdout block | Rejected: each greeting requires its own wrapper |
| Modify the greeting library | Rejected: formatting is CLI-only |
| Wrap the composed message once before repeat | Selected: preserves transform and newline order with minimal work |

## Security Considerations

No shell evaluation, escaping, sanitization, network access, or sensitive state is introduced. Existing validation remains authoritative.

## Performance Considerations

Form the optional wrapped message once before repetition. Do not add a second output buffer or recompute the transformation for each repetition.

## Testing Strategy

Exactly two independent pytest-bdd scenarios map AC1 and AC2 to SCN001 and SCN002. Use the existing CLI main/capsys conventions and exact stdout, stderr, and exit-status assertions. The second scenario checks both composed absence and the default invocation. Supplementary CLI unit coverage may exercise literal content preservation; retain existing behavior tests rather than adding more BDD scenarios.

Run the repository-required pytest, feature-suite, and Ruff commands during implementation verification, not specification publication.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Uppercasing prefix or wrapping the entire repeated block | SCN001 asserts two separately wrapped greetings with a lower-case prefix |
| Changing default bytes or the final LF | SCN002 asserts exact composed and default outputs |
| Expanding scope to stopped fixtures | Do not implement or revise any other issue |

## Open Questions

None. VERSION is delivery-owner only, excluded from implementation authority; preserve dynamic version metadata and the current major line.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #102 | 2026-09-07 | Initial feature spec |
