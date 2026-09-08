# Design: Add nmg-smoke braces flag

**Issue**: #105
**Date**: 2026-09-08
**Status**: Approved
**Author**: NMG

---

## Overview

Implement the requirements in the existing thin argparse adapter. Keep the pure greeting library unchanged; no new dependencies or helper layer.

## Architecture

### Data Flow

1. Parse long-only boolean --braces using store_true, default false, alongside existing options.
2. Obtain and validate the greeting through the existing path.
3. Apply uppercase to the greeting, prepend the literal prefix, and apply optional parentheses in that existing order.
4. When braces are enabled, wrap the complete message once in literal { and }, outside any parentheses regardless of flag ordering.
5. Reuse repeat and newline emission unchanged.

## API / Interface Changes

| Interface | Input | Output |
|-----------|-------|--------|
| nmg-smoke | --braces, no value, no short alias, default false | Each fully formatted greeting enclosed in literal curly braces |

Preserve existing signatures, validation, errors, and positional-name requirement. Prefix text is not uppercased. Existing braces, parentheses, and internal newlines in content are preserved literally without escaping, stripping, or normalization. Wrap the message, not each physical line or the entire repeated stdout block.

## Database / Storage Changes

None.

## State Management

Only an invocation-local argparse boolean; no persistent state.

## UI Components

Argparse exposes the new CLI flag in help; no graphical UI.

## Alternatives Considered

| Option | Decision |
|--------|----------|
| Wrap the repeated output block | Rejected: every greeting needs its own braces |
| Wrap before parentheses | Rejected: braces must be outermost |
| Wrap the fully formatted message once before repeat | Selected: minimal and preserves existing semantics |

## Security Considerations

No shell evaluation, network access, or sensitive state. Existing validation remains authoritative.

## Performance Considerations

Build the wrapped message once before repetition; no second output buffer or per-repetition formatting.

## Testing Strategy

Exactly two independent pytest-bdd scenarios map AC1/AC2 to SCN001/SCN002. Follow existing main/capsys step conventions and assert exact stdout, empty stderr, and exit 0. SCN001 covers composition with every existing formatting flag. SCN002 checks both parentheses-composed output and the bare default without braces. Supplementary unit coverage is limited to a meaningful literal-content preservation edge case. Run repository-required pytest, BDD, and Ruff checks during implementation verification, never during authoring.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Incorrect nesting or uppercase prefix | SCN001 asserts literal lowercase prefix inside parentheses inside braces |
| Wrapping repeated block or changing final LF | SCN001 asserts separately wrapped greetings and no final LF |
| Default output changes | SCN002 asserts exact composed and default bytes |

## Open Questions

None. VERSION remains delivery-owner only on v3. No other issue is implemented or revised.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #105 | 2026-09-08 | Initial feature spec |
