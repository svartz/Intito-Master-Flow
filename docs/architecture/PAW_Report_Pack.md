# IMF PAW Report Pack

## Purpose

This document defines the source-controlled PAW workbook baseline for IMF.

The repo now contains report-pack specifications under:

- [`src/paw-reports/IMF.PAW.MasterFlow.Workbook.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Workbook.json)
- [`src/paw-reports/IMF.PAW.MasterFlow.Views.json`](/c:/Programming/Intito-Master-Flow/src/paw-reports/IMF.PAW.MasterFlow.Views.json)

These files are not exported PAW workbooks. They are deterministic workbook and view specifications intended for:

- architecture review
- Git-based change tracking
- deployment scripting later
- alignment between UI design and IMF process/cube design

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
