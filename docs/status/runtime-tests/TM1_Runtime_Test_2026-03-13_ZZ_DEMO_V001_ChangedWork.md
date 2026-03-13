# TM1 Runtime Test 2026-03-13 - Changed Work Version

Scenario:
- Tenant: `OWPOF99JMW8L`
- Database: `IMF`
- Dimension code: `ZZ_DEMO`
- Version id: `V001`
- Work dimension: `ZZ_DEMO_VER_V001`
- Change applied in work dimension only: added element `ZZ_DEMO_EDIT_001`

Processes executed:
1. `IMF.P.Compare.VersionToMaster`
2. `IMF.P.Validate.Technical`
3. `IMF.P.Impact.RunAll`
4. `IMF.P.Commit.Prepare`
5. `IMF.P.PAW.SyncRuntime`

Execution result:
- `IMF.P.Compare.VersionToMaster`: `CompletedSuccessfully`
- `IMF.P.Validate.Technical`: `CompletedSuccessfully`
- `IMF.P.Impact.RunAll`: `CompletedSuccessfully`
- `IMF.P.Commit.Prepare`: `CompletedSuccessfully`
- `IMF.P.PAW.SyncRuntime`: `CompletedSuccessfully`

TM1 log files:
- `ProcessLog_20260313183617_1773426977000_IMF.P.Compare.VersionToMaster.jsonl`
- `ProcessLog_20260313183618_1773426978000_IMF.P.Validate.Technical.jsonl`
- `ProcessLog_20260313183618_17734269780000_IMF.P.Impact.RunAll.jsonl`
- `ProcessLog_20260313183619_1773426979000_IMF.P.Commit.Prepare.jsonl`
- `ProcessLog_20260313183701_1773427021000_IMF.P.PAW.SyncRuntime.jsonl`

Observed IMF records:
- `IMF.D.DiffRecord` contains `DIFF|V001|ELEMENT|ADD|ZZ_DEMO_EDIT_001`
- `IMF.D.ImpactRecord` contains `IMP|V001|SUMMARY`

Observed PAW runtime result:
- `IMF.PAW.V.Impact` returned a populated row with:
  - `Severity = WARNING`
  - `ObjectName = ZZ_DEMO`
  - `ImpactDomain = SUMMARY`
  - message `Impact includes non-destructive changes that should be reviewed before publish.`
- `IMF.PAW.V.Validation` returned a populated row with:
  - `Severity = BLOCKER`
  - `RuleCode = APPROVAL_REQUIRED`
  - `ValidationType = BUSINESS`
  - message `Publish requires an approved version.`

Interpretation:
- A real work-dimension change now flows through compare, impact, commit preparation, and PAW runtime views.
- `IMF.P.Compare.Elements` needed `IMF.P.Control.EnsureRecord` to be first-run safe when creating new diff records.
- PAW runtime views show the updated findings after `IMF.P.PAW.SyncRuntime` refreshes the public subsets and views.

Open observation:
- The current PAW runtime uses rebuilt public subsets for record-driven tabs.
- New diff or impact records do not automatically appear in PAW views until `IMF.P.PAW.SyncRuntime` is executed again.
