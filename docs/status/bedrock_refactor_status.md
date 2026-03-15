# IMF Bedrock Refactor Status

## Purpose

This document summarizes the current Bedrock adoption status for IMF.

The authoritative machine-readable register is:

- [IMF_Bedrock_Refactor_Register.yaml](/c:/Git/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Refactor_Register.yaml)

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

1. `IMF.P.Dimension.Create` - verified parameter mapping implemented in source
2. `IMF.P.Dimension.Clear` - direct Bedrock call intentionally disabled until a wrapper exists
3. `IMF.P.Dimension.CopyRelations` - verified hierarchy-clone parameter mapping implemented for single-hierarchy flow
4. `IMF.P.Attribute.CopyDefinitions` - verified attribute-create parameter mapping implemented
5. `IMF.P.Security.CreateGroups` - verified group-create parameter mapping implemented
6. `IMF.P.Security.SetCubeAccess` - verified object-assign parameter mapping implemented
7. `IMF.P.Security.SetDimensionAccess` - verified object-assign parameter mapping implemented
8. `IMF.P.Log.Event` - verified server-log parameter mapping implemented

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
## Parameter verification

Bedrock parameter contracts used by IMF are now verified against the Bedrock 5 GitHub repository.

Reference artifacts:
- [IMF_Bedrock_Parameter_Spec.md](/c:/Git/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Parameter_Spec.md)
- [IMF_Bedrock_Parameter_Mismatch.csv](/c:/Git/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Parameter_Mismatch.csv)

Current result:
- `IMF.P.Dimension.Create`: fixed to use `pDim`
- `IMF.P.Dimension.Clear`: no longer makes an invalid direct Bedrock call
- `IMF.P.Dimension.CopyRelations`: fixed to use `pSrcDim`, `pSrcHier`, `pTgtDim`, `pTgtHier`
- `IMF.P.Attribute.CopyDefinitions`: fixed to use `pDim`, `pAttr`, `pAttrType`
- `IMF.P.Security.CreateGroups`: fixed to use `pGroup`
- `IMF.P.Security.SetCubeAccess`: fixed to use `pGroup`, `pObjectType`, `pObject`, `pSecurityLevel`
- `IMF.P.Security.SetDimensionAccess`: fixed to use `pGroup`, `pObjectType`, `pObject`, `pSecurityLevel`
- `IMF.P.Log.Event`: fixed to use `pLevel` and `pMessage`
