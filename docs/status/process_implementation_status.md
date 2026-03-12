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
| Dimension operations | partial | Native create, clear, and relation replay baselines now exist; multi-hierarchy and Bedrock contract work remain. |
| Attributes | partial | Native definition/value copy baselines now exist; publish semantics and Bedrock contract confirmation remain. |
| Diff | partial | Version-to-master diff baselines now write records to `IMF.C.Diff`; severity tuning and richer semantics remain. |
| Validation | partial | Technical/business validation shells exist with targeted TODOs. |
| Impact | partial | Process graph exists, but blocker classification remains lightweight. |
| Publish / rollback | partial | Baseline archive, publish, and rollback structure-copy flows now exist; production hardening and safety checks remain. |
| Security | partial | Strong scaffold coverage through phase 3, still environment-dependent in several areas. |
| Import / export | partial | Contracts exist, full payload parsing and replay remain incomplete. |
| Logging | partial | Logging entry points exist, but TM1 persistence targets remain TODO-driven. |

## Priority Focus

Refactor or complete these first:

1. `IMF.P.Commit.Prepare`
2. `IMF.P.Impact.*`
3. `IMF.P.Security.Apply*` and `IMF.P.Security.Validate*`
4. `IMF.P.Log.Event` and `IMF.P.Log.Change`
5. `IMF.P.Text.Import`
6. `IMF.P.Attribute.Publish`

## Update Rule

Whenever a process changes status materially:

- update this document
- update `docs/releases/unreleased.md`
- update release notes if the change is part of a cut release
