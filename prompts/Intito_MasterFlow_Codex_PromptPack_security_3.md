# Codex Task: IMF Security Hardening

Extend the existing Intito MasterFlow (IMF) security model with enterprise-grade hardening.

This is Phase 3 of the IMF security implementation.

Previous phases implemented:
1 Security structure
2 Security implementation

Phase 3 must implement:

- element-level security
- version ownership enforcement
- dimension masking
- audit logging
- security validation automation
- security regression testing

The implementation must be compatible with:

IBM Planning Analytics / TM1 v12  
Git-based DevOps deployment  
JSON-based TM1 object representation  

---

# Repository Structure

Use the existing repository layout.

src/
  tm1/
    processes/
    cubes/
    dimensions/
    subsets/

docs/
  security/

All TI processes must be created in:

src/tm1/processes/

Do not generate processes outside this folder.

---

# IMF Security Roles

The following groups already exist and must be used:

IMF_Admin  
IMF_Developer  
IMF_Operator  
IMF_Approver  
IMF_Editor  
IMF_Viewer  
IMF_Auditor  
IMF_Service  

Never grant security directly to individual users.

All security must be group-based.

---

# Hardening Objectives

Implement the following additional controls:

1 Element Security
2 Version Ownership Security
3 Dimension Visibility Controls
4 Security Audit Trail
5 Security Validation Processes
6 Security Regression Tests

---

# 1 Element Security

Introduce element-level security for IMF work dimensions.

Scope:

IMF managed dimensions

Examples:

Product  
Customer  
CostCenter  

Work versions:

*_WRK_*

Archive versions:

*_ARC_*

---

## Required Behavior

Editors should only modify elements within their authorized work versions.

Approvers should have read-only access.

Viewers should not see draft work versions unless explicitly permitted.

---

## Implementation

Create a security model using:

element security cubes

Pattern:

}ElementSecurity_<Dimension>

Processes must generate element security assignments based on:

Version ownership  
Version status  
User group  

---

# Required Processes

Create:

IMF.P.Security.ApplyElementSecurity  
IMF.P.Security.ValidateElementSecurity  

---

# 2 Version Ownership Security

Implement ownership enforcement for dimension work versions.

Only the version owner or authorized operators may modify a work version.

---

## Ownership Metadata

Ownership is stored in:

IMF.C.Version

Fields:

VersionID  
Owner  
Status  
LockedBy  

---

## Enforcement

Implement validation that:

Editors can modify only:

their own versions  
versions assigned to their group  

Operators can modify any version.

Approvers cannot modify versions.

---

# Required Processes

Create:

IMF.P.Security.ValidateVersionOwnership  
IMF.P.Security.ApplyVersionOwnershipSecurity  

---

# 3 Dimension Masking

Prevent certain roles from seeing internal IMF dimensions.

Sensitive dimensions include:

IMF.D.Run  
IMF.D.ChangeType  
IMF.D.ImpactType  

Viewers should not see operational dimensions.

Editors should see only required dimensions.

---

# Required Processes

Create:

IMF.P.Security.ApplyDimensionMasking  
IMF.P.Security.ValidateDimensionMasking  

---

# 4 Security Audit Trail

Create a security audit logging framework.

All security operations must log events.

Target cube:

IMF.C.EventLog

If unavailable, use structured log files.

---

## Events to Log

Security bootstrap  
Group validation  
Cube security assignment  
Dimension security assignment  
Element security changes  
Ownership violations  
Security validation failures  

---

# Required Processes

Create:

IMF.P.Security.LogSecurityEvent  
IMF.P.Security.ExportSecurityAudit  

---

# 5 Security Validation

Create automated security validation processes.

These must verify:

Required groups exist  
Cube security is correct  
Dimension security is correct  
Element security rules exist  
Ownership rules are enforced  

---

# Required Processes

Create:

IMF.P.Security.ValidateFullModel  
IMF.P.Security.ValidateCubeSecurity  
IMF.P.Security.ValidateDimensionSecurity  

---

# 6 Security Regression Testing

Create automated security regression tests.

Purpose:

Detect security drift after deployment.

These tests must verify:

Editors cannot publish  
Viewers cannot modify dimensions  
Approvers cannot edit versions  
Developers cannot bypass security in PROD  

---

# Required Processes

Create:

IMF.P.Security.TestAccessEditor  
IMF.P.Security.TestAccessViewer  
IMF.P.Security.TestAccessApprover  
IMF.P.Security.RunSecurityRegressionSuite  

---

# Environment Awareness

Processes must support parameter:

pEnvironment

Values:

DEV  
TEST  
PROD  

Behavior:

DEV  
Relaxed security validation.

TEST  
Strict validation warnings.

PROD  
Strict enforcement.

---

# JSON Process Format

Each TI process must also produce a JSON representation.

Example:

processName.ti  
processName.json  

JSON must include:

name  
purpose  
parameters  
prolog  
metadata  
tags  

Tags:

IMF  
Security  
Hardening  
TM1  
PAW  
v12  

JSON formatting must be deterministic for Git.

---

# Documentation

Update documentation in:

docs/security/

Files:

IMF_Security_Model.md  
IMF_Security_Hardening.md  
IMF_Security_Matrix.csv  
IMF_Process_Security_Matrix.csv  

---

# Documentation Content

Document:

Element security rules  
Ownership rules  
Dimension masking strategy  
Audit trail design  
Security validation approach  
Security regression tests  

---

# Coding Rules

Use consistent naming.

Do not invent unsupported TM1 functions.

Where environment-specific implementation is required:

Mark with TODO.

Ensure code is readable and structured.

Avoid hardcoded users.

---

# Final Output

After generating files:

1 List all created processes
2 List all updated documentation
3 List remaining TODO markers
4 Describe assumptions about TM1 security configuration
5 Confirm compatibility with Git deployment