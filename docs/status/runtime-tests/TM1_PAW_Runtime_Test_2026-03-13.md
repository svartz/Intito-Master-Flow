# TM1 PAW Runtime Test 2026-03-13

Environment:
- Tenant: `OWPOF99JMW8L`
- Database: `IMF`

Processes deployed:
- `IMF.P.PAW.BuildSubsets`
- `IMF.P.PAW.BuildViews`
- `IMF.P.PAW.SyncRuntime`

Execution result:
- `IMF.P.PAW.SyncRuntime`: `CompletedSuccessfully`
- Log file: `ProcessLog_20260313180945_1773425385000_IMF.P.PAW.SyncRuntime.jsonl`

Verified public subsets:
- `IMF.PAW.SS.Version.Open`
- `IMF.PAW.SS.ValidationMeasure.OpenVersionMeasures`
- `IMF.PAW.SS.ImpactMeasure.SummaryMeasures`

Verified public views:
- `IMF.PAW.V.Overview`
- `IMF.PAW.V.Versions`
- `IMF.PAW.V.Validation`
- `IMF.PAW.V.Impact`

Interpretation:
- The first PAW runtime pack is now materialized in TM1, not only stored as repo specifications.
- The current runtime baseline covers the first operational workbook tabs: overview, versions, validation, and impact.
