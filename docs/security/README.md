# IMF Security Package

## Security model overview
This package defines a production-oriented, group-based IMF security model for TM1 / Planning Analytics v12.

## Role descriptions
IMF_Admin, IMF_Developer, IMF_Operator, IMF_Approver, IMF_Editor, IMF_Viewer, IMF_Auditor, IMF_Service.

## Bootstrap instructions
Run IMF.P.Security.BootstrapAll with pEnvironment, pCreateIfExistsBehavior, pStrictMode, pLogToCube, and pLogFile.

## Validation instructions
Run IMF.P.Security.ValidateGroups and IMF.P.Security.ValidateObjectSecurity.

## DEV / TEST / PROD differences
DEV allows broader developer rights. TEST is near-production. PROD applies strict least privilege.

## External IAM assumptions
Group creation may be external to TM1. The package does not fake successful creation.

## Source-control package
The corresponding TI processes live in src/tm1/processes/ and are delivered as both .ti and .json artefacts.