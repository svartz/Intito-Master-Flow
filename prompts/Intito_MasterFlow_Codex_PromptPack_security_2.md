
---

# Required Processes

Generate the following processes:

### Bootstrap

IMF.P.Security.BootstrapAll

### Group provisioning

IMF.P.Security.CreateGroups  
IMF.P.Security.CreateSingleGroup  
IMF.P.Security.ValidateGroups

### Security assignment

IMF.P.Security.ApplyModel  
IMF.P.Security.SetCubeAccess  
IMF.P.Security.SetDimensionAccess

### Security export

IMF.P.Security.ExportProcessMatrix  
IMF.P.Security.ExportSecurityMatrix

### Validation / audit

IMF.P.Security.ValidateObjectSecurity  
IMF.P.Security.LogBootstrap

---

# Implementation Requirements

## 1 Group Creation

Implement group creation logic as far as possible for TM1 v12.

If group provisioning depends on external identity provider:

DO NOT fake creation.

Instead:

Validate group existence  
Log missing groups  
Support strict validation mode

Parameters:

pStrictMode = Y | N

Behavior:

Strict mode
Abort bootstrap if required group missing

Non-strict mode
Log warning and continue

---

# 2 Cube Security

Implement cube security using the IMF model.

Target cubes:

IMF.C.Config  
IMF.C.Version  
IMF.C.Diff  
IMF.C.Validation  
IMF.C.Impact  
IMF.C.EventLog  
IMF.C.ChangeLog  
IMF.C.PublishHistory

Required access model:

| Cube | Admin | Dev | Operator | Approver | Editor | Viewer | Auditor |
|-----|-----|-----|-----|-----|-----|-----|-----|
| IMF.C.Config | WRITE | READ | READ | READ | NONE | NONE | READ |
| IMF.C.Version | WRITE | WRITE | WRITE | READ | READ | READ | READ |
| IMF.C.Diff | WRITE | WRITE | WRITE | READ | READ | READ | READ |
| IMF.C.Validation | WRITE | WRITE | WRITE | READ | READ | READ | READ |
| IMF.C.Impact | WRITE | WRITE | WRITE | READ | READ | READ | READ |
| IMF.C.EventLog | WRITE | WRITE | WRITE | READ | READ | READ | READ |
| IMF.C.ChangeLog | WRITE | WRITE | WRITE | READ | READ | READ | READ |
| IMF.C.PublishHistory | WRITE | READ | WRITE | READ | READ | READ | READ |

Use:

IMF_Admin  
IMF_Developer  
IMF_Operator  
IMF_Approver  
IMF_Editor  
IMF_Viewer  
IMF_Auditor

---

# 3 Dimension Security

Apply rules for:

### Control dimensions

IMF.D.*

Access:

Admin WRITE  
All others READ

### Master dimensions

Pattern:

Configured IMF managed dimensions

Access:

Admin ADMIN  
Others READ

### Work dimensions

Pattern:

_WRK_

Access:

Admin WRITE  
Developer WRITE  
Operator WRITE  
Approver READ  
Editor WRITE  
Viewer NONE  
Auditor READ

### Archive dimensions

Pattern:

_ARC_

Access:

Admin WRITE  
Operator READ  
Approver READ  
Editor NONE  
Viewer NONE  
Auditor READ

---

# 4 Process Security

Generate a matrix describing which roles may run which process.

Categories:

Version processes  
Compare processes  
Validation processes  
Impact processes  
Commit processes  
Rollback processes  
Export processes  
Import processes  
Security processes

Export to:

docs/security/IMF_Process_Security_Matrix.csv

---

# 5 Environment Awareness

Processes must support:

pEnvironment

Values:

DEV  
TEST  
PROD

Rules:

DEV

Developers may have broader rights

TEST

Near production

PROD

Strict least privilege

---

# 6 Logging

All security processes must log events.

Preferred cube:

IMF.C.EventLog

Fallback:

ASCIIOutput log file.

Parameters:

pLogToCube  
pLogFile

Log:

Start  
Warnings  
Security assignments  
Validation results  
Errors  
Completion

---

# 7 Validation

Implement validation processes:

IMF.P.Security.ValidateGroups  
IMF.P.Security.ValidateObjectSecurity

These must:

Verify groups exist  
Verify cube security  
Verify dimension security  
Export mismatches

Export format:

docs/security/IMF_Security_Matrix.csv

Fields:

ObjectType  
ObjectName  
Group  
ExpectedAccess  
ActualAccess  
Status  
Comment

---

# 8 JSON Representation

Each process JSON must include:

name  
purpose  
parameters  
prolog  
metadata  
tags  
environmentScope

Tags:

IMF  
Security  
TM1  
PAW  
v12

JSON must be deterministic and Git-friendly.

---

# 9 Documentation

Update:

docs/security/IMF_Security_Model.md  
docs/security/IMF_Security_Matrix.csv  
docs/security/IMF_Process_Security_Matrix.csv  
docs/security/README.md

README must include:

Security model overview  
Role descriptions  
Bootstrap instructions  
Validation instructions  
DEV / TEST / PROD differences  
External IAM assumptions

---

# 10 Implementation Style

Code must be:

Readable  
Deterministic  
Git friendly  
Group based only

Never grant permissions to individual users.

Where direct TM1 security manipulation depends on environment:

Add clear TODO markers.

---

# Final Output

After generation:

1 List all files created
2 List completed TODOs
3 List remaining environment-dependent TODOs
4 List assumptions about TM1 security configuration
5 Confirm compatibility with Git deployment