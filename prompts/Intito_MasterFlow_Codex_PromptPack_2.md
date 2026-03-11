# Codex Master Task: Complete All IMF TI Process Logic

You are working in the Intito MasterFlow (IMF) repository for IBM Planning Analytics / TM1 v12.

Your task is to complete the logic in **all IMF TI processes** so the process library moves from scaffold/pseudo-implementation to implementation-ready source.

The repository is already structured and contains IMF process scaffolds, documentation, and security assets.

You must:
1. read the existing repository and infer current status of each IMF TI process
2. complete missing logic in all IMF TI processes
3. preserve naming, structure, and repo conventions
4. generate or update matching `.ti` and `.json` files for all processes
5. keep the implementation compatible with Git-based TM1 DevOps workflows
6. be honest where environment-specific dependencies still require explicit TODO markers

Do not rewrite the architecture. Implement the logic.

---

# Repository Layout

Use this repository structure exactly:

src/
  tm1/
    processes/
    cubes/
    dimensions/
    subsets/
    chores/

docs/
  architecture/
  security/
  object_catalog/
  adr/

tests/
  unit/
  integration/
  regression/

All TI process files must live in:

src/tm1/processes/

Do not create TI files anywhere else.

---

# File Format Rules

For every IMF process there must be two files:

- `<ProcessName>.ti`
- `<ProcessName>.json`

Example:

- `IMF.P.Commit.PublishVersion.ti`
- `IMF.P.Commit.PublishVersion.json`

The `.json` representation must be deterministic and Git-friendly.

Each `.json` file must include at minimum:
- `name`
- `purpose`
- `parameters`
- `prolog`
- `metadata`
- `tags`
- `environmentScope`

Required tags:
- `IMF`
- `TM1`
- `PAW`
- `v12`

Add tags such as:
- `Security`
- `Versioning`
- `Validation`
- `Impact`
- `Publish`
- `Rollback`
- `Import`
- `Export`
where relevant.

---

# Naming and Design Rules

Keep all existing IMF object names unchanged.

All process names must remain under:
- `IMF.P.*`

Do not invent a new naming scheme.

Do not hardcode user names.

Use group- or metadata-driven design where security or ownership is involved.

Do not pretend unsupported TM1 functions exist.
If a capability depends on environment-specific TM1 setup, identity provider integration, external IAM, or deployment tooling:
- leave a clear `TODO:`
- implement validation and export logic around it
- do not fake success

---

# Primary Objective

Complete the logic in **all IMF TI processes**, including at least the following areas:

## 1. Versioning
Complete logic for:
- creating new work versions
- cloning from master
- cloning from existing version
- locking and unlocking versions
- deleting draft versions safely
- updating version metadata
- logging version lifecycle events

Target processes include:
- `IMF.P.Version.Create`
- `IMF.P.Version.CloneFromMaster`
- `IMF.P.Version.CloneFromVersion`
- `IMF.P.Version.Lock`
- `IMF.P.Version.Unlock`
- `IMF.P.Version.Delete`

## 2. Dimension Copying
Complete logic for:
- creating target dimension
- clearing/rebuilding target dimension
- copying elements
- copying hierarchies/relations
- copying weights
- copying aliases
- copying attributes
- preserving supported structure conventions

Target processes include:
- `IMF.P.Dimension.CopyAll`
- `IMF.P.Dimension.Create`
- `IMF.P.Dimension.Clear`
- `IMF.P.Dimension.CopyRelations`

## 3. Attribute Handling
Complete logic for:
- attribute definition discovery
- attribute type handling
- alias handling
- copying attribute values
- comparing attributes
- publishing attributes from work to master

Target processes include:
- `IMF.P.Attribute.CopyDefinitions`
- `IMF.P.Attribute.CopyValues`
- `IMF.P.Attribute.Compare`
- `IMF.P.Attribute.Publish`

## 4. Diff Engine
Complete logic for:
- element comparison
- relation comparison
- weight comparison
- attribute comparison
- alias comparison
- writing structured diff output
- writing change log entries

Target processes include:
- `IMF.P.Compare.VersionToMaster`
- `IMF.P.Compare.Elements`
- `IMF.P.Compare.Relations`
- `IMF.P.Compare.Attributes`

Write output to the intended IMF diff and change-tracking structures if they exist.
If exact target objects differ in the repo, adapt to repo reality instead of inventing new names.

## 5. Validation
Complete logic for:
- technical validation
- business validation
- mandatory attribute checks
- uniqueness checks
- orphan detection
- invalid hierarchy checks
- alias collision checks
- publishability prechecks

Target processes include:
- `IMF.P.Validate.Technical`
- `IMF.P.Validate.Business`
- `IMF.P.Validate.Attributes`

## 6. Impact Analysis
Complete logic for:
- cube impact analysis
- view impact analysis
- subset impact analysis
- process impact analysis
- security impact analysis
- integration impact analysis
- severity classification
- blocker detection

Target processes include:
- `IMF.P.Impact.RunAll`
- `IMF.P.Impact.Cubes`
- `IMF.P.Impact.Views`
- `IMF.P.Impact.Subsets`
- `IMF.P.Impact.Processes`
- `IMF.P.Impact.Security`
- `IMF.P.Impact.Integrations`

Impact results must support:
- Info
- Warning
- Error
- Blocker

## 7. Publish / Archive / Rollback
Complete logic for:
- pre-publish validation
- archive-before-publish
- publishing work version to master
- publish finalization
- rollback validation
- rollback execution
- rollback snapshot creation
- publish/rollback history logging

Target processes include:
- `IMF.P.Commit.Prepare`
- `IMF.P.Commit.ArchiveMaster`
- `IMF.P.Commit.PublishVersion`
- `IMF.P.Commit.Finalize`
- `IMF.P.Rollback.Validate`
- `IMF.P.Rollback.ToArchive`

Do not allow publish to proceed if blocker-level impact issues exist.

## 8. Security
Complete logic for:
- security bootstrap support
- group validation
- cube access model
- dimension access model
- process security matrix export
- object security validation
- bootstrap logging

Target processes include:
- `IMF.P.Security.BootstrapAll`
- `IMF.P.Security.CreateGroups`
- `IMF.P.Security.CreateSingleGroup`
- `IMF.P.Security.ApplyModel`
- `IMF.P.Security.SetCubeAccess`
- `IMF.P.Security.SetDimensionAccess`
- `IMF.P.Security.ExportProcessMatrix`
- `IMF.P.Security.ExportSecurityMatrix`
- `IMF.P.Security.ValidateGroups`
- `IMF.P.Security.ValidateObjectSecurity`
- `IMF.P.Security.LogBootstrap`

Respect the IMF group naming model:
- `IMF_Admin`
- `IMF_Developer`
- `IMF_Operator`
- `IMF_Approver`
- `IMF_Editor`
- `IMF_Viewer`
- `IMF_Auditor`
- `IMF_Service`

## 9. Import / Export
Complete logic for:
- CSV parent-child export
- CSV leaf-flat export
- JSON parent-child export
- JSON leaf-flat export
- SQL parent-child export
- SQL leaf-flat export
- CSV import
- JSON import
- SQL import
- staging normalization
- leaf-flat to hierarchy normalization
- payload generation and parsing
- configurable output/input targets

Target processes include:
- `IMF.P.Export.CSV.ParentChild`
- `IMF.P.Export.CSV.LeafFlat`
- `IMF.P.Export.JSON.ParentChild`
- `IMF.P.Export.JSON.LeafFlat`
- `IMF.P.Export.SQL.ParentChild`
- `IMF.P.Export.SQL.LeafFlat`
- `IMF.P.Import.CSV.ParentChild`
- `IMF.P.Import.CSV.LeafFlat`
- `IMF.P.Import.JSON.ParentChild`
- `IMF.P.Import.JSON.LeafFlat`
- `IMF.P.Import.SQL.ParentChild`
- `IMF.P.Import.SQL.LeafFlat`

## 10. Logging
Complete logic for:
- event logging
- change logging
- severity/status logging
- fallback file logging if log cube unavailable
- consistent timestamp handling
- correlation/run id handling

Target processes include:
- `IMF.P.Log.Event`
- `IMF.P.Log.Change`

---

# Environment and Deployment Awareness

Support environment-aware behavior where relevant.

Use:
- `DEV`
- `TEST`
- `PROD`

Rules:
- `DEV` may allow more developer flexibility
- `TEST` should be close to production
- `PROD` must enforce strict least privilege and stricter validation

Keep implementation compatible with Git-based TM1 DevOps workflows.

Preserve or improve determinism of `.json` files and avoid unstable formatting.

---

# Completion Rules

A process is only considered complete if all of the following are true:

1. its `.ti` file contains meaningful implementation logic, not only placeholders
2. its `.json` file matches the `.ti` content
3. obvious TODO placeholders are either:
   - implemented, or
   - narrowed to a specific environment-dependent dependency
4. parameter handling is explicit
5. logging and error handling are present where needed
6. the process participates correctly in the IMF end-to-end workflow

Do not stop after editing a subset of files.
Work through the full IMF TI process library.

---

# Verification Requirements

Before finishing, perform a verification pass across the repository.

You must:
1. identify every IMF process file in `src/tm1/processes/`
2. confirm each has both `.ti` and `.json`
3. confirm naming matches exactly
4. confirm no process remains scaffold-only unless explicitly environment-blocked
5. confirm there are no inconsistent group names
6. confirm publish/rollback/security flows are internally consistent
7. confirm security, validation, impact and logging processes are connected correctly

If tests already exist in the repo, update them where needed.
If tests do not exist for critical paths, create or extend tests under:
- `tests/unit/`
- `tests/integration/`
- `tests/regression/`

Focus at minimum on:
- version creation
- diff generation
- validation
- impact analysis
- publish
- rollback
- security bootstrap
- security validation

---

# Documentation Updates

Update relevant docs if implementation changes behavior.

At minimum review and update, if needed:
- `docs/architecture/*`
- `docs/security/*`
- `docs/object_catalog/*`

If you modify assumptions, document them clearly.

---

# Coding Style

Be explicit, conservative, and implementation-focused.

Prefer:
- readable TI
- deterministic JSON
- clear comments
- exact TODOs only when unavoidable
- narrow, honest environment assumptions

Avoid:
- fake success handling
- unsupported invented TM1 APIs
- introducing new IMF object names without need
- partial completion without reporting remaining gaps

---

# Final Output Contract

When done, return:

## 1. Summary
A concise summary of what was implemented.

## 2. Files changed
List every file created or modified.

## 3. Processes completed
List all IMF TI processes completed.

## 4. Remaining TODOs
List only the TODOs that are truly environment-dependent.

## 5. Assumptions
List assumptions about:
- TM1 v12 environment
- security model
- external IAM / CAM / SSO
- deployment mechanism
- object naming

## 6. Verification result
State whether:
- all processes now have `.ti` and `.json`
- all critical workflows are connected
- any blockers remain

Work until the IMF TI process library is fully completed or until only genuinely environment-specific blockers remain.