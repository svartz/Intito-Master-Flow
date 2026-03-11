
# Intito MasterFlow Codex Runbook

This runbook orchestrates the full implementation of Intito MasterFlow using Codex.

## Step 1 – Initialize Core Metadata
Create the following objects:
- IMF.D.Dimension
- IMF.D.Version
- IMF.D.Status
- IMF.C.Config
- IMF.C.Version

## Step 2 – Version Engine
Implement:
- IMF.P.Version.Create
- IMF.P.Version.CloneFromMaster
- IMF.P.Version.CloneFromVersion
- IMF.P.Version.Lock
- IMF.P.Version.Unlock

## Step 3 – Dimension Copy Engine
Processes:
- IMF.P.Dimension.CopyAll
- IMF.P.Attribute.CopyDefinitions
- IMF.P.Attribute.CopyValues

## Step 4 – Diff Engine
Process:
- IMF.P.Compare.VersionToMaster

Detect:
- Added elements
- Deleted elements
- Changed parents
- Attribute changes

## Step 5 – Validation Engine
Process:
- IMF.P.Validate.Technical
- IMF.P.Validate.Business

Checks:
- Mandatory attributes
- Duplicate keys
- Invalid hierarchies

## Step 6 – Impact Analysis
Processes:
- IMF.P.Impact.Cubes
- IMF.P.Impact.Views
- IMF.P.Impact.Subsets
- IMF.P.Impact.Processes
- IMF.P.Impact.Security
- IMF.P.Impact.Integrations

## Step 7 – Publish Engine
Processes:
- IMF.P.Commit.ArchiveMaster
- IMF.P.Commit.PublishVersion

## Step 8 – Rollback Engine
Processes:
- IMF.P.Rollback.Validate
- IMF.P.Rollback.ToArchive

## Step 9 – Export Engine
Processes:
- IMF.P.Export.CSV.ParentChild
- IMF.P.Export.CSV.LeafFlat
- IMF.P.Export.JSON.ParentChild
- IMF.P.Export.JSON.LeafFlat
- IMF.P.Export.SQL.ParentChild
- IMF.P.Export.SQL.LeafFlat

## Step 10 – Import Engine
Processes:
- IMF.P.Import.CSV.ParentChild
- IMF.P.Import.CSV.LeafFlat
- IMF.P.Import.JSON.ParentChild
- IMF.P.Import.JSON.LeafFlat
- IMF.P.Import.SQL.ParentChild
- IMF.P.Import.SQL.LeafFlat

After each step:
1. Run unit tests
2. Commit to Git
3. Update object catalog
