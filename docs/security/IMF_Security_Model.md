# IMF Security Model

## Scope
This package defines the Intito MasterFlow security model for IBM Planning Analytics / TM1 v12 in a Git-reviewable source format.

## IMF groups
- IMF_Admin
- IMF_Developer
- IMF_Operator
- IMF_Approver
- IMF_Editor
- IMF_Viewer
- IMF_Auditor
- IMF_Service

## Environment behavior
- DEV: developers may receive broader write access for selected configuration and governance parameters.
- TEST: mirror PROD closely while still allowing controlled validation.
- PROD: apply least privilege and restrict write access to platform-critical settings.

## TODO sections
- TODO: connect group creation and validation to the target IAM or TM1 security provider
- TODO: confirm native }CubeSecurity intersection order before enabling direct CellPutS writes
- TODO: confirm native }DimensionSecurity intersection order before enabling direct CellPutS writes
- TODO: resolve logical dimension classes such as MasterDimensions and WorkDimensions to actual deployed objects
- TODO: implement read-back validation of actual object security from TM1 control cubes
- TODO: mirror bootstrap logs into IMF.C.EventLog once the target cube design is finalized

## Assumptions
- IMF security is group-based only; no direct user grants are created
- LogOutput is available in the target TM1 environment
- some IMF cubes referenced by the model may be introduced later than this package