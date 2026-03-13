# TM1 Runtime Test 2026-03-13

Scenario:
- Tenant: `OWPOF99JMW8L`
- Database: `IMF`
- Dimension code: `ZZ_DEMO`
- Version id: `V001`

Processes executed:
1. `IMF.P.Compare.VersionToMaster`
2. `IMF.P.Validate.Technical`
3. `IMF.P.Impact.RunAll`
4. `IMF.P.Commit.Prepare`

Execution result:
- `IMF.P.Compare.VersionToMaster`: `CompletedSuccessfully`
- `IMF.P.Validate.Technical`: `CompletedSuccessfully`
- `IMF.P.Impact.RunAll`: `CompletedSuccessfully`
- `IMF.P.Commit.Prepare`: `CompletedSuccessfully`

TM1 log files:
- `ProcessLog_20260313154325_1773416605000_IMF.P.Compare.VersionToMaster.jsonl`
- `ProcessLog_20260313154327_1773416607000_IMF.P.Validate.Technical.jsonl`
- `ProcessLog_20260313154328_1773416608000_IMF.P.Impact.RunAll.jsonl`
- `ProcessLog_20260313154330_1773416610000_IMF.P.Commit.Prepare.jsonl`

Latest rerun log files:
- `ProcessLog_20260313155952_1773417592000_IMF.P.Compare.VersionToMaster.jsonl`
- `ProcessLog_20260313155952_17734175920000_IMF.P.Validate.Technical.jsonl`
- `ProcessLog_20260313155953_1773417593000_IMF.P.Impact.RunAll.jsonl`
- `ProcessLog_20260313155954_1773417594000_IMF.P.Commit.Prepare.jsonl`

Latest first-run deterministic log files:
- `ProcessLog_20260313180436_1773425076000_IMF.P.Validate.Business.jsonl`
- `ProcessLog_20260313180437_1773425077000_IMF.P.Impact.RunAll.jsonl`
- `ProcessLog_20260313180438_1773425078000_IMF.P.Commit.Prepare.jsonl`

Observed error messages:
- None in this rerun.

Observed process outcome:
- `IMF.P.Commit.Prepare` finished without TM1 error messages, but ended with `ProcessBreak()`.
- `IMF.P.Commit.Prepare` parameters at `ProcessBreak()`:
  - `pPrefix = IMF`
  - `pDimensionCode = ZZ_DEMO`
  - `pVersionId = V001`
- Version status after the run: `Blocked`
- Version notes after the run: `Publish preparation detected blocker-level validation or impact findings.`
- Approval state after the run: `Pending`

Interpretation:
- The runtime sequence now executes cleanly in TM1.
- The final blocked state is business logic, not a runtime failure.
- The current scenario is blocked because publish preparation found blocker-level findings and the version is still pending approval.
- The previous first-run issue for business validation and impact summary records is fixed locally through `IMF.P.Control.EnsureRecord`.
