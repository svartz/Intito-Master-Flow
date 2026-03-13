# IMF PAW Report Pack

## Purpose

This document defines the source-controlled PAW workbook baseline for IMF.

The repo now contains report-pack specifications under:

- [`src/paw-reports/IMF.PAW.MasterFlow.Workbook.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Workbook.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Views.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Views.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Subsets.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Subsets.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Actions.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Actions.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Runtime.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Runtime.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Layout.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Layout.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Deployment.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Deployment.json)

These files are not exported PAW workbooks. They are deterministic workbook and view specifications intended for:

- architecture review
- Git-based change tracking
- deployment scripting later
- alignment between UI design and IMF process/cube design

The current PAW track now includes:

- workbook navigation and tab contract
- view-to-cube binding
- default subset contract per tab
- process-action contract for compare, validate, impact, and publish preparation
- runtime contract for public subsets and public views
- workbook layout contract per tab
- deployment contract for target PAW book creation
- builder processes:
  - `IMF.P.PAW.BuildSubsets`
  - `IMF.P.PAW.BuildViews`
  - `IMF.P.PAW.SyncRuntime`
  - `IMF.P.PAW.SyncRuntimeIfPresent`

The current runtime baseline now covers:

- `Overview`
- `Versions`
- `Editing`
- `Validation`
- `Impact`
- `Publish`
- `Archive`
- `Rollback`
- `Exchange`

## Workbook Baseline

Workbook:

- `IMF.PAW.MasterFlow`

Tabs:

1. `Overview`
2. `Versions`
3. `Editing`
4. `Validation`
5. `Impact`
6. `Publish`
7. `Archive`
8. `Rollback`
9. `Export/Import`

## Design Rules

- technical object names remain stable and untranslated
- tab labels and help text resolve through IMF text keys
- the default language is `en-US`
- the fallback language is `en-US`
- supported languages follow the IMF language model

## Deployment Boundary

Native PAW workbook generation is environment-specific and is not automated in this repo yet.

The current implementation therefore stops at source-controlled report definitions. A future deployment step can transform these specs into:

- PAW books
- PAW views
- PAW navigation tiles
- localized workbook captions
