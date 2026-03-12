# IMF Remaining Work Plan

## Purpose

This document captures the next implementation waves after the current baseline hardening of:

- dimension replay
- attribute copy
- diff generation
- publish archive/replace flow
- rollback backup/restore flow
- source-controlled PAW workbook specifications

## Current Baseline

The repo now has a working source-level baseline for:

- native dimension structure replay
- native attribute definition and value replay
- baseline diff records in `IMF.C.Diff`
- baseline archive, publish, and rollback structure-copy orchestration

The model is still not production-complete. The remaining work is concentrated in environment-sensitive controls, blocker semantics, and runtime validation.

## Wave A - Release Safety

Priority: highest

1. Harden `IMF.P.Commit.Prepare`
   - stop publish when validation or impact contains blocker-level findings
   - define severity contract in `IMF.C.Impact` and `IMF.C.Validation`
2. Harden `IMF.P.Validate.Technical`
   - add duplicate key checks
   - add orphan and invalid-hierarchy checks
   - add alias-collision checks
3. Harden `IMF.P.Validate.Business`
   - define explicit business rule findings
   - classify blocking vs non-blocking findings

## Wave B - Security Activation

Priority: highest

1. Complete `IMF.P.Security.SetCubeAccess`
   - confirm native `}CubeSecurity` writeback contract
   - implement read-back validation
2. Complete `IMF.P.Security.SetDimensionAccess`
   - confirm `}DimensionSecurity` writeback contract
   - implement wildcard/class resolution
3. Complete `IMF.P.Security.ApplyElementSecurity`
   - resolve `}ElementSecurity_<Dimension>` writeback pattern
4. Complete `IMF.P.Security.Validate*`
   - compare documented policy against actual assigned security

## Wave C - Logging And Audit Persistence

Priority: high

1. Finalize `IMF.P.Log.Event`
   - persist to `IMF.C.EventLog`
2. Finalize `IMF.P.Log.Change`
   - persist to `IMF.C.ChangeLog`
3. Add event ids / audit linkage
   - connect publish, rollback, compare, and security flows to shared run ids

## Wave D - Import / Export Completion

Priority: high

1. Complete `IMF.P.Text.Import`
   - wire the datasource and row validation
2. Complete exchange processes
   - parse and replay CSV, JSON, and SQL payloads
3. Add validation around export/import contracts
   - shape, delimiter, schema, and reject behavior

## Wave E - Bedrock Stabilization

Priority: medium

1. Confirm Bedrock contracts for:
   - `}bedrock.dim.create`
   - `}bedrock.dim.clone`
   - `}bedrock.hier.clone`
   - `}bedrock.dim.attr.create`
   - `}bedrock.security.group.create`
   - `}bedrock.security.object.assign`
   - `}bedrock.server.writetomessagelog`
2. Move Wave 1 processes from seam-level support to verified delegation
3. Reassess Tier 2 candidates:
   - `IMF.P.Dimension.CopyAll`
   - `IMF.P.Attribute.CopyValues`
   - `IMF.P.Commit.ArchiveMaster`
   - `IMF.P.Security.ApplyModel`

## Wave F - PAW Runtime Deployment

Priority: medium

1. Transform `src/paw-reports/` specs into deployable PAW assets
2. Bind workbook views to deployed cubes and dimensions
3. Apply IMF text-key localization to workbook labels and help text

## Wave G - Verification

Priority: highest before PROD

1. Add TM1 runtime test execution in a DEV environment
2. Validate publish and rollback on real dimensions
3. Validate diff output on controlled master/work fixtures
4. Validate security with real groups and effective-access readback
5. Validate localized PAW behavior against the deployed model
