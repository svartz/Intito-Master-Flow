# IMF Process Implementation Status

## Status Scale

- `scaffold`
- `partial`
- `implementation-ready`
- `verified`

## Current Baseline

This document should be updated whenever a meaningful IMF process implementation change lands in `src/processes/`.

## Domain Summary

| Domain | Current status | Notes |
|---|---|---|
| Versioning | partial | Core flows exist, but several processes still contain TM1-environment TODOs. |
| Dimension operations | partial | Utility helpers now exist; relation traversal remains a key gap. |
| Attributes | partial | Compare/publish helpers exist, but deep attribute logic is not fully complete. |
| Diff | partial | Structure exists, but compare semantics remain scaffold-heavy. |
| Validation | partial | Technical/business validation shells exist with targeted TODOs. |
| Impact | partial | Process graph exists, but blocker classification remains lightweight. |
| Publish / rollback | partial | Core orchestration exists, but safe production semantics need hardening. |
| Security | partial | Strong scaffold coverage through phase 3, still environment-dependent in several areas. |
| Import / export | partial | Contracts exist, full payload parsing and replay remain incomplete. |
| Logging | partial | Logging entry points exist, but TM1 persistence targets remain TODO-driven. |

## Priority Focus

Refactor or complete these first:

1. `IMF.P.Dimension.CopyRelations`
2. `IMF.P.Attribute.CopyDefinitions`
3. `IMF.P.Attribute.CopyValues`
4. `IMF.P.Compare.*`
5. `IMF.P.Commit.PublishVersion`
6. `IMF.P.Rollback.ToArchive`

## Update Rule

Whenever a process changes status materially:

- update this document
- update `docs/releases/unreleased.md`
- update release notes if the change is part of a cut release
