# Design: Add LIVE_SMOKE_214_A managed steering verification marker

**Issue**: #30
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

## Overview

Add one repository-root regular text file. The fixed data artifact has no runtime dependencies or control flow.

## Verification

Read the file as bytes and compare it with `Buffer.from('LIVE_SMOKE_214_A\n', 'utf8')`. Run the existing Jest suite. Delivery may update `VERSION`, `package.json`, and `CHANGELOG.md` under the repository's automatic version contract.

The marker aligns with `steering/product.md` evidence-led delivery, follows the Jest gate in `steering/tech.md`, and respects `steering/structure.md` by adding no runtime, workflow, agent, or script surface.
