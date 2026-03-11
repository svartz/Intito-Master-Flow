# IMF Security Hardening

## Scope
Phase 3 hardens the IMF security package with element-level controls, ownership enforcement, masking, audit logging, validation automation, and regression testing.

## Element security
- Work versions (`*_WRK_*`) are intended to be writable only for the version owner or delegated editor scope.
- Archive versions (`*_ARC_*`) are intended to be read-only for approvers and auditors and hidden from viewers when policy requires it.
- Actual `}ElementSecurity_<Dimension>` assignment remains environment-specific and is marked with `TODO` in the TI processes.

## Version ownership
- Ownership metadata is assumed to live in `IMF.C.Version`.
- `IMF.P.Security.ApplyVersionOwnershipSecurity` and `IMF.P.Security.ValidateVersionOwnership` model the enforcement boundary.
- Operators are expected to retain break-glass access.

## Dimension masking
- Sensitive operational dimensions include `IMF.D.Run`, `IMF.D.ChangeType`, and `IMF.D.ImpactType`.
- Viewers should not see operational dimensions.
- Editors should only see dimensions needed for assigned workflows.

## Audit trail
- `IMF.P.Security.LogSecurityEvent` emits structured security events.
- `IMF.P.Security.ExportSecurityAudit` provides a review/export surface.
- `IMF.C.EventLog` integration remains a documented `TODO` until cube grain is finalized.

## Validation automation
- `IMF.P.Security.ValidateFullModel` orchestrates groups, cube security, dimension security, masking, element security, and ownership checks.
- Validation outputs align to `ObjectType,ObjectName,Group,ExpectedAccess,ActualAccess,Status,Comment`.

## Regression testing
- `IMF.P.Security.RunSecurityRegressionSuite` orchestrates role-based regression tests.
- Current tests cover Editor, Viewer, and Approver scenarios.
- Developer bypass detection in PROD remains a `TODO` pending impersonation or a controlled session test harness.
