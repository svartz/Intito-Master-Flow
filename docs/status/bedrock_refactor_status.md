# IMF Bedrock Refactor Status

## Purpose

This document summarizes the current Bedrock adoption status for IMF.

The authoritative machine-readable register is:

- [IMF_Bedrock_Refactor_Register.yaml](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Refactor_Register.yaml)

## Current Phase

- Phase: wave 1 started
- Implementation status: facade implementation started

Implemented in source:

- `IMF.P.Dimension.Create` now supports opt-in Bedrock delegation with native fallback
- `IMF.P.Dimension.Clear` now supports opt-in Bedrock delegation with native fallback
- `IMF.P.Dimension.CopyRelations` now supports opt-in Bedrock delegation and explicit IMF fallback TODO boundaries
- `IMF.P.Log.Event` now supports opt-in Bedrock server-log delegation with native fallback
- `IMF.P.Attribute.CopyDefinitions` now includes Bedrock-ready orchestration and explicit contract checkpoints for attribute-definition delegation
- `IMF.P.Security.CreateGroups` now supports Bedrock-aware group provisioning orchestration
- `IMF.P.Security.SetCubeAccess` now supports Bedrock-aware security assignment orchestration
- `IMF.P.Security.SetDimensionAccess` now supports Bedrock-aware security assignment orchestration

## Tier 1 Targets

These should be refactored first:

1. `IMF.P.Dimension.Create`
2. `IMF.P.Dimension.Clear`
3. `IMF.P.Dimension.CopyRelations`
4. `IMF.P.Attribute.CopyDefinitions`
5. `IMF.P.Security.CreateGroups`
6. `IMF.P.Security.SetCubeAccess`
7. `IMF.P.Security.SetDimensionAccess`
8. `IMF.P.Log.Event`

Current wave 1 state:

1. `IMF.P.Dimension.Create` - hybridized in source
2. `IMF.P.Dimension.Clear` - hybridized in source
3. `IMF.P.Dimension.CopyRelations` - in progress
4. `IMF.P.Attribute.CopyDefinitions` - in progress
5. `IMF.P.Security.CreateGroups` - in progress
6. `IMF.P.Security.SetCubeAccess` - in progress
7. `IMF.P.Security.SetDimensionAccess` - in progress
8. `IMF.P.Log.Event` - hybridized in source

## Tier 2 Targets

- `IMF.P.Dimension.CopyAll`
- `IMF.P.Attribute.CopyValues`
- `IMF.P.Version.CloneFromMaster`
- `IMF.P.Version.CloneFromVersion`
- `IMF.P.Commit.ArchiveMaster`
- `IMF.P.Security.ApplyModel`

## Tier 3 Targets

These stay primarily IMF-owned:

- `IMF.P.Version.*` lifecycle orchestration
- `IMF.P.Commit.*` publish orchestration
- `IMF.P.Rollback.*`
- `IMF.P.Compare.*`
- `IMF.P.Validate.*`
- `IMF.P.Impact.*`
- `IMF.P.Security.Validate*`
- `IMF.P.Security.Test*`

## Update Rule

Whenever Bedrock adoption status changes:

- update the YAML register first
- update this summary second
- note the change in `docs/releases/unreleased.md`
