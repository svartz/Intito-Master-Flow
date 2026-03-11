# IMF Security Model

## Security model overview
This package defines a production-oriented, group-based IMF security model for TM1 / Planning Analytics v12 and extends it with Phase 3 hardening controls.

## Role descriptions
- IMF_Admin: full control
- IMF_Developer: development/support role with broader access only in DEV
- IMF_Operator: operational workflow role
- IMF_Approver: approval review role
- IMF_Editor: controlled work-version editor
- IMF_Viewer: least-privilege read-only role
- IMF_Auditor: audit-focused read-only role
- IMF_Service: service automation role

## Hardening controls
- Element security is applied to managed work and archive dimensions through `}ElementSecurity_<Dimension>`.
- Version ownership enforcement uses Owner, Status, and LockedBy metadata from `IMF.C.Version`.
- Dimension masking hides operational dimensions such as `IMF.D.Run`, `IMF.D.ChangeType`, and `IMF.D.ImpactType` from low-privilege roles.
- Security operations emit structured audit events through `IMF.P.Security.LogSecurityEvent`.
- Validation runs through `IMF.P.Security.ValidateFullModel`.
- Regression coverage runs through `IMF.P.Security.RunSecurityRegressionSuite`.

## Bootstrap instructions
Run `IMF.P.Security.BootstrapAll` with `pEnvironment`, `pCreateIfExistsBehavior`, `pStrictMode`, `pLogToCube`, and `pLogFile`.

## Validation instructions
Run `IMF.P.Security.ValidateFullModel`, then review `IMF_Security_Matrix.csv`, `IMF_Process_Security_Matrix.csv`, and `IMF_Security_Audit.csv`.

## DEV / TEST / PROD differences
- DEV: developers may receive broader rights and validation is relaxed.
- TEST: warnings are strict and close to production.
- PROD: strict least privilege and no developer bypass.

## External IAM assumptions
- Group creation may be external to TM1.
- The package does not fake successful group creation.
- Strict mode aborts bootstrap if required groups are missing and cannot be validated.

## Remaining environment-dependent TODOs
- Connect group existence checks and provisioning to the target IAM or TM1 provider.
- Confirm the exact native write pattern for `}CubeSecurity`.
- Confirm the exact native write pattern for `}DimensionSecurity`.
- Confirm the exact native write pattern for `}ElementSecurity_<Dimension>`.
- Implement read-back validation of actual security assignments and session-based regression execution.
- Mirror logging into `IMF.C.EventLog` once the cube grain is finalized.
