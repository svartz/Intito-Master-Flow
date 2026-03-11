# IMF Security Model

## Security model overview
This package defines a production-oriented, group-based IMF security model for TM1 / Planning Analytics v12.

## Role descriptions
- IMF_Admin: full control
- IMF_Developer: development/support role with broader access only in DEV
- IMF_Operator: operational workflow role
- IMF_Approver: approval review role
- IMF_Editor: controlled work-version editor
- IMF_Viewer: least-privilege read-only role
- IMF_Auditor: audit-focused read-only role
- IMF_Service: service automation role

## Bootstrap instructions
Run IMF.P.Security.BootstrapAll with pEnvironment, pCreateIfExistsBehavior, pStrictMode, pLogToCube, and pLogFile.

## Validation instructions
Run IMF.P.Security.ValidateGroups and IMF.P.Security.ValidateObjectSecurity, then review IMF_Security_Matrix.csv and IMF_Process_Security_Matrix.csv.

## DEV / TEST / PROD differences
- DEV: developers may receive broader rights.
- TEST: near-production behavior.
- PROD: strict least privilege.

## External IAM assumptions
- Group creation may be external to TM1.
- The package does not fake successful group creation.
- Strict mode aborts bootstrap if required groups are missing and cannot be validated.

## Remaining environment-dependent TODOs
- Connect group existence checks and provisioning to the target IAM or TM1 provider.
- Confirm the exact native write pattern for }CubeSecurity.
- Confirm the exact native write pattern and wildcard resolution for }DimensionSecurity.
- Implement read-back validation of actual security assignments.
- Mirror logging into IMF.C.EventLog once the cube grain is finalized.