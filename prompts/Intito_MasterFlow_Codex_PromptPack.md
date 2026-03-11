# Codex Prompt Pack – Intito MasterFlow

This prompt pack contains step-by-step tasks to let Codex implement the Intito MasterFlow framework for TM1 / Planning Analytics.

---

## 1. Initialize Project

**Prompt**

Read the architecture documentation and object catalog.  
Create the base TM1 objects for Intito MasterFlow.

Create:

- IMF.D.Dimension
- IMF.D.Version
- IMF.D.Status
- IMF.C.Config
- IMF.C.Version

Requirements:

- Follow naming standard IMF.*
- No hardcoded dimension names
- All processes must be parameter driven

Output:

- dimension definitions
- cube definitions

---

## 2. Implement Version.Create

**Prompt**

Implement process:

IMF.P.Version.Create

Purpose:

Create a new work version of a dimension.

Inputs:

- DimensionCode
- VersionId
- SourceType (MASTER | VERSION)

Outputs:

- Work dimension created

Requirements:

- Metadata written to IMF.C.Version
- Event logged to IMF.C.EventLog

---

## 3. Implement CloneFromMaster

**Prompt**

Implement process:

IMF.P.Version.CloneFromMaster

Function:

Clone master dimension into work version.

Process must copy:

- elements
- parent-child relations
- weights
- attribute definitions
- attribute values
- aliases

---

## 4. Implement Diff Engine

**Prompt**

Create process:

IMF.P.Compare.VersionToMaster

Purpose:

Compare work dimension with master.

Detect:

- added elements
- deleted elements
- moved elements
- changed attributes
- changed aliases
- changed weights

Write results to:

- IMF.C.Diff
- IMF.C.ChangeLog

---

## 5. Implement Validation

**Prompt**

Create process:

IMF.P.Validate.Technical

Checks:

- mandatory attributes
- duplicate keys
- invalid hierarchy
- orphan elements
- alias collisions

Write errors to:

IMF.C.Validation

---

## 6. Implement Impact Analysis

**Prompt**

Create process:

IMF.P.Impact.RunAll

Impact domains:

- cubes
- views
- subsets
- processes
- security
- integrations

Write results to:

IMF.C.Impact

Severity levels:

- Info
- Warning
- Error
- Blocker

---

## 7. Implement Publish Engine

**Prompt**

Create process:

IMF.P.Commit.PublishVersion

Flow:

1. Validate version
2. Check impact analysis
3. Archive master
4. Replace master dimension
5. Log publish event

Outputs:

- Updated master dimension
- Archive dimension created

---

## 8. Implement Archive Engine

**Prompt**

Create process:

IMF.P.Commit.ArchiveMaster

Archive naming:

<Dimension>_ARC_<timestamp>

Process must:

- clone master dimension
- store archive name in version metadata

---

## 9. Implement Rollback

**Prompt**

Create processes:

- IMF.P.Rollback.Validate
- IMF.P.Rollback.ToArchive

Rollback flow:

1. Validate archive dimension
2. Run impact analysis
3. Archive current master
4. Restore archive as new master
5. Log rollback

---

## 10. Implement Export Engine

**Prompt**

Create export processes:

- IMF.P.Export.CSV.ParentChild
- IMF.P.Export.CSV.LeafFlat

Support formats:

- CSV
- JSON
- SQL
- HTTP

Data shapes:

- ParentChild
- LeafFlat