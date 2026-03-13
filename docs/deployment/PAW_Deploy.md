# PAW Deploy

## Purpose

This document describes the current deploy flow for IMF PAW workbook specifications.

The repo now contains a deterministic PAW packaging utility:

- [`tools/paw_deploy.py`](/c:/Programming/Intito-Master-Flow/tools/paw_deploy.py)

The utility does not create native PAW books directly yet. It validates and packages the PAW source specifications into a deploy bundle that can later be transformed or consumed by a PAW-specific automation step.

## Supported Commands

Validate the workbook package:

```powershell
python tools/paw_deploy.py validate
```

Print a workbook deployment plan:

```powershell
python tools/paw_deploy.py plan
```

Build a deterministic deploy bundle:

```powershell
python tools/paw_deploy.py build-bundle
```

Output:

- `build/paw/IMF.PAW.MasterFlow.bundle.json`

## What Is Validated

- workbook tabs exist in layout pages
- layout widgets reference known views and actions
- runtime spec references a real builder process
- deployment spec dependencies point to the expected workbook artifacts

## Current Boundary

The current PAW deploy flow stops at a versioned deploy bundle.

It does not yet:

- call a native PAW workbook API
- import a workbook into PAW directly
- resolve layout widgets into a vendor-specific workbook payload

That is deliberate. The current objective is to keep the PAW layer deterministic, reviewable in Git, and ready for a later PAW-native deployment adapter.
