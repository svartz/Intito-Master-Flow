# IMF Bedrock Adoption Design

## Purpose
This document describes how Bedrock v5 should be used in IMF deployments to accelerate and harden the IMF TI process library without replacing IMF's domain-specific control model.

## Executive Summary
Bedrock should be adopted as an implementation utility layer for TM1-common operations:

- dimension and hierarchy creation and cloning
- attribute and alias utility work
- standard logging
- generic security object assignment
- subset and export helpers

IMF should remain the orchestration and domain layer for:

- version lifecycle
- publish, archive, and rollback workflow
- diff semantics
- business validation
- impact analysis
- ownership and approval rules
- IMF control-cube updates

The recommended model is:

1. `IMF.P.*` remains the public process library.
2. `IMF.P.*` calls Bedrock processes for low-level TM1 operations.
3. IMF control cubes and metadata remain the source of truth for workflow state.
4. Bedrock is never allowed to bypass IMF validation, ownership, or publish gates.

## Why Bedrock Is Relevant
Bedrock v5 provides a mature set of reusable TI utilities for TM1 engineering. For IMF, that is attractive because the current process library still contains many implementation-ready scaffolds where the repetitive TM1 mechanics are not yet fully implemented.

Bedrock can reduce custom code volume in exactly the areas that are expensive and repetitive:

- dimension lifecycle operations
- security assignment plumbing
- log writing
- metadata utility behavior

Bedrock should not become the IMF architecture. It should become an internal accelerator.

## Adoption Principles

### Principle 1: IMF Owns the Business Contract
IMF processes keep their names, parameters, and orchestration role.

Examples:

- `IMF.P.Version.Create`
- `IMF.P.Commit.PublishVersion`
- `IMF.P.Rollback.ToArchive`
- `IMF.P.Security.ValidateFullModel`

These processes continue to be the repo's public and documented automation surface.

### Principle 2: Bedrock Owns Reusable TM1 Mechanics
Bedrock is used where the problem is a generic TM1 operation, not an IMF-specific workflow.

Examples:

- create or clone a dimension
- assign security to an object
- write structured log output
- create groups
- work with element attributes and aliases

### Principle 3: No Bedrock Lock-In at Workflow Boundaries
IMF orchestration should call Bedrock in narrow seams rather than turning whole workflows into Bedrock wrappers.

Good:

- `IMF.P.Dimension.Create` calling a Bedrock create utility
- `IMF.P.Security.SetCubeAccess` calling Bedrock object-security assignment

Bad:

- replacing `IMF.P.Commit.PublishVersion` with a direct Bedrock clone-and-swap pattern that bypasses IMF gates

### Principle 4: Bedrock Calls Must Be Parameterized and Traceable
Every IMF process that delegates to Bedrock should:

- validate inputs first
- log what Bedrock process is called
- log failure context
- preserve deterministic repo behavior
- keep environment-specific dependencies behind explicit `TODO:` markers

## Target Architecture

### Layer 1: IMF Domain Layer
These processes remain IMF-owned:

- `IMF.P.Version.*`
- `IMF.P.Commit.*`
- `IMF.P.Rollback.*`
- `IMF.P.Compare.*`
- `IMF.P.Validate.Business`
- `IMF.P.Impact.*`
- ownership, masking, and regression processes under `IMF.P.Security.*`

Responsibilities:

- workflow state
- publish and rollback gates
- status transitions
- lineage and notes
- impact severity interpretation
- ownership and approval enforcement
- writeback to IMF control structures

### Layer 2: IMF Utility Facade
These are IMF processes that should become Bedrock-backed first:

- `IMF.P.Dimension.Create`
- `IMF.P.Dimension.Clear`
- `IMF.P.Dimension.CopyRelations`
- `IMF.P.Attribute.CopyDefinitions`
- `IMF.P.Attribute.CopyValues`
- `IMF.P.Security.CreateGroups`
- `IMF.P.Security.SetCubeAccess`
- `IMF.P.Security.SetDimensionAccess`
- `IMF.P.Log.Event`

Responsibilities:

- adapt IMF parameters to Bedrock parameter contracts
- isolate Bedrock usage from the rest of the repo
- keep future replacement possible

### Layer 3: Bedrock Runtime Layer
This is the imported Bedrock package in the target IMF environment.

Expected usage categories:

- `}bedrock.dim.*`
- `}bedrock.hier.*`
- `}bedrock.dim.attr.*`
- `}bedrock.security.*`
- `}bedrock.server.*`
- subset or export utilities where needed

## Recommended Bedrock Usage by Capability

### Versioning
Use Bedrock indirectly.

Bedrock is suitable for:

- creating the technical target dimension
- cloning a master or source dimension
- logging technical actions

Bedrock is not suitable as the owner of:

- version status transitions
- IMF.C.Version updates
- ownership and locking semantics
- publishability gates

### Dimension Copying
Use Bedrock heavily.

This is the strongest adoption area because the current IMF library still leaves much of the low-level dimension traversal and rebuild behavior as TODOs.

Preferred pattern:

1. `IMF.P.Dimension.Create` delegates to a Bedrock dimension create utility.
2. `IMF.P.Dimension.Clear` delegates to a Bedrock clear or rebuild-safe pattern where available.
3. `IMF.P.Dimension.CopyAll` orchestrates.
4. `IMF.P.Dimension.CopyRelations` delegates relation replay and weight handling to Bedrock-capable hierarchy utilities.

### Attribute Handling
Use Bedrock selectively.

Bedrock should help with:

- attribute definition creation
- alias handling
- possibly alias swap or attribute utility operations

IMF should continue to own:

- compare semantics against master
- publish semantics
- diff writeback to IMF structures

### Diff Engine
Use Bedrock minimally.

The diff engine is IMF-specific. Bedrock may assist with reading structure, but the meaning of a change in IMF belongs to IMF.

Examples:

- added element
- deleted element
- changed parent
- attribute change
- alias change
- publish blocker or warning classification

### Validation
Use Bedrock minimally to moderately.

Technical validation may use Bedrock utility checks where available, but business validation must remain IMF-owned.

### Impact Analysis
Do not move this to Bedrock.

Impact analysis is tightly coupled to IMF governance, blocker logic, and repo-specific deployment semantics.

### Publish / Archive / Rollback
Use Bedrock only for low-level structure operations.

The orchestration itself remains IMF-owned.

### Security
Use Bedrock substantially for generic security plumbing.

Good Bedrock candidates:

- group creation
- object security assignment
- standardized log writing

IMF still owns:

- IMF role model
- ownership enforcement
- masking policy
- regression test semantics

### Import / Export
Use Bedrock selectively.

Bedrock may help with generic file and metadata utility patterns, but IMF-specific parent-child, leaf-flat, JSON, and SQL contracts must remain IMF-owned.

## Concrete Mapping Strategy
See:

- [IMF_Bedrock_Process_Mapping.csv](/c:/Git/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Process_Mapping.csv)
- [IMF_Bedrock_Refactor_Register.yaml](/c:/Git/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Refactor_Register.yaml)

Summary:

- `Tier 1`: refactor first, strong Bedrock fit
- `Tier 2`: refactor second, mixed fit
- `Tier 3`: IMF-owned, only selective Bedrock usage

## Refactor Order

### Wave 1
Refactor first because they have high utility value, low business-risk coupling, and strong Bedrock fit:

- `IMF.P.Dimension.Create`
- `IMF.P.Dimension.Clear`
- `IMF.P.Dimension.CopyRelations`
- `IMF.P.Attribute.CopyDefinitions`
- `IMF.P.Security.CreateGroups`
- `IMF.P.Security.SetCubeAccess`
- `IMF.P.Security.SetDimensionAccess`
- `IMF.P.Log.Event`

### Wave 2
Refactor next because they benefit from Bedrock but still require IMF orchestration around them:

- `IMF.P.Dimension.CopyAll`
- `IMF.P.Attribute.CopyValues`
- `IMF.P.Version.CloneFromMaster`
- `IMF.P.Version.CloneFromVersion`
- `IMF.P.Commit.ArchiveMaster`
- `IMF.P.Security.ApplyModel`

### Wave 3
Keep mostly IMF-owned:

- `IMF.P.Version.Create`
- `IMF.P.Commit.Prepare`
- `IMF.P.Commit.PublishVersion`
- `IMF.P.Commit.Finalize`
- `IMF.P.Rollback.*`
- `IMF.P.Compare.*`
- `IMF.P.Validate.*`
- `IMF.P.Impact.*`
- `IMF.P.Security.Validate*`
- `IMF.P.Security.Test*`

## Refactor Rules for IMF Developers

When refactoring an IMF process to Bedrock:

1. Do not rename the IMF process.
2. Do not change the IMF process purpose.
3. Keep the IMF process as the public entry point.
4. Add explicit comments describing Bedrock delegation.
5. Log before and after Bedrock calls.
6. Preserve IMF control-cube writes in IMF-owned code.
7. Keep environment-dependent Bedrock assumptions behind targeted `TODO:` markers.

## Risks

### Version Risk
Bedrock v5 must be aligned with the exact IMF target TM1 v12 patch level.

### Behavioral Risk
Generic Bedrock dimension operations may not exactly match IMF publish, archive, or diff semantics.

### Security Risk
Security assignment utilities must not weaken IMF ownership or masking rules.

### Maintenance Risk
If IMF processes call Bedrock directly everywhere, the repo becomes harder to reason about. That is why the utility-facade approach is recommended.

## Decision
Adopt Bedrock v5 in IMF as a controlled utility layer under the IMF process library, starting with dimension, attribute, logging, and security plumbing.

Do not adopt Bedrock as the workflow owner for versioning, publish, rollback, validation, impact, or IMF-specific diff logic.
