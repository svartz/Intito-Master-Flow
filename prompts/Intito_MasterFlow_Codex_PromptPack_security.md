# Codex Master Prompt – IMF Security Model for TM1 / Planning Analytics v12

Implement the complete security model for **Intito MasterFlow (IMF)** in **IBM Planning Analytics / TM1 v12**.

## Goal
Create a production-oriented security package for IMF that:
1. defines all required IMF security groups
2. provisions those groups consistently
3. applies cube security
4. applies dimension security
5. exports a process security matrix
6. documents parameter governance
7. delivers all TI processes in **both `.ti` and `.json` format** for v12-compatible source control / Git workflows

Use the existing IMF naming standard and security design below.

---

## Naming rules
All IMF security groups must start with `IMF_`.

Required groups:
- `IMF_Admin`
- `IMF_Developer`
- `IMF_Operator`
- `IMF_Approver`
- `IMF_Editor`
- `IMF_Viewer`
- `IMF_Auditor`
- `IMF_Service`

All new security-related processes must start with:
- `IMF.P.Security.`

All output files must use the same process name in both formats:
- `IMF.P.Security.CreateGroups.ti`
- `IMF.P.Security.CreateGroups.json`

Do not introduce any non-prefixed role names.

---

## Deliverables
Create the following files under:

- `src/ti_processes/`
- `docs/security/`

For every TI process, generate:
1. a `.ti` file
2. a `.json` file
3. matching names and metadata

Also generate:
- `docs/security/IMF_Security_Model.md`
- `docs/security/IMF_Security_Matrix.csv`
- `docs/security/IMF_Process_Security_Matrix.csv`
- `docs/security/README.md`

---

## Required TI processes

Create these processes:

### Group provisioning
- `IMF.P.Security.BootstrapAll`
- `IMF.P.Security.CreateGroups`
- `IMF.P.Security.CreateSingleGroup`

### Object security
- `IMF.P.Security.ApplyModel`
- `IMF.P.Security.SetCubeAccess`
- `IMF.P.Security.SetDimensionAccess`

### Export / documentation
- `IMF.P.Security.ExportProcessMatrix`
- `IMF.P.Security.ExportSecurityMatrix`

### Validation / audit
- `IMF.P.Security.ValidateGroups`
- `IMF.P.Security.ValidateObjectSecurity`
- `IMF.P.Security.LogBootstrap`

---

## Required behavior

### 1. Group creation
Implement logic or environment-adaptable placeholders for provisioning the required `IMF_` groups.

Support parameter:
- `pCreateIfExistsBehavior` = `SKIP` | `RECREATE`

If direct creation of groups depends on environment or identity provider, make the process:
- validate existence
- log missing groups
- clearly mark environment-specific sections with `TODO`
- avoid fake "success" logic

### 2. Cube security
Apply the following recommended cube access model:

| Cube | IMF_Admin | IMF_Developer | IMF_Operator | IMF_Approver | IMF_Editor | IMF_Viewer | IMF_Auditor |
|---|---|---|---|---|---|---|---|
| IMF.C.Config | WRITE | READ | READ | READ | NONE | NONE | READ |
| IMF.C.Version | WRITE | WRITE | WRITE | READ | READ |
| IMF.C.Diff | WRITE | WRITE | WRITE | READ | READ |
| IMF.C.Validation | WRITE | WRITE | WRITE | READ | READ |
| IMF.C.Impact | WRITE | WRITE | WRITE | READ | READ |
| IMF.C.EventLog | WRITE | WRITE | WRITE | READ | READ |
| IMF.C.ChangeLog | WRITE | WRITE | WRITE | READ | READ |
| IMF.C.PublishHistory | WRITE | READ | WRITE | READ | READ |

Assume `IMF_Viewer` and `IMF_Auditor` should have READ where appropriate unless the cube is explicitly hidden.

### 3. Dimension security
Apply the following recommended dimension access model:

| Dimension class | IMF_Admin | IMF_Developer | IMF_Operator | IMF_Approver | IMF_Editor | IMF_Viewer | IMF_Auditor |
|---|---|---|---|---|---|---|---|
| IMF.D.* control dimensions | WRITE/READ | READ | READ | READ | READ | READ | READ |
| master dimensions | ADMIN/READ | READ | READ | READ | READ | READ | READ |
| work dimensions | ADMIN/WRITE | WRITE | WRITE | READ | WRITE (restricted) | NONE/READ | READ |
| archive dimensions | ADMIN/WRITE | READ | READ | READ | NONE/READ | NONE | READ |

### 4. Parameter governance
Document and implement placeholders/control logic for these parameter classes:

#### Platform-critical parameters
Examples:
- archive policy
- rollback policy
- require impact analysis
- require approval
- max open versions
- endpoint configuration

Access:
- `IMF_Admin` = WRITE
- `IMF_Developer` = READ, or WRITE in DEV only
- everyone else = READ or NONE according to least privilege

#### Dimension governance parameters
Examples:
- `AllowDelete`
- `AllowCreateElement`
- `AllowReparent`
- `MandatoryAttributes`
- `LeafKeyAttribute`

Access:
- `IMF_Admin` = WRITE
- `IMF_Operator` = optional WRITE if configured
- `IMF_Developer` = WRITE in DEV only, READ in PROD
- `IMF_Editor` = NONE

#### Version metadata
Examples:
- description
- owner
- lock state
- comments
- approval status

Access:
- `IMF_Admin`, `IMF_Developer`, `IMF_Operator` = WRITE
- `IMF_Approver` = WRITE only for approval fields
- `IMF_Editor` = WRITE only on own / authorized versions
- `IMF_Viewer`, `IMF_Auditor` = READ only

### 5. Environment-aware behavior
Support parameter:
- `pEnvironment` = `DEV` | `TEST` | `PROD`

Rules:
- `DEV`: developers may have broader access, including WRITE to selected config objects
- `TEST`: close to PROD
- `PROD`: strict least-privilege model

### 6. Logging
All bootstrap and apply operations must write clear log entries or placeholder log calls to:
- `IMF.C.EventLog`
or equivalent IMF logging mechanism

Do not silently skip failed actions.

---

## File format requirements for v12

For each TI process, output:

### A. `.ti`
A readable TI source file containing:
- process name
- purpose
- parameter list
- prolog
- metadata placeholders
- clearly marked `TODO` blocks for environment-specific implementation

### B. `.json`
A JSON representation of the same process containing at minimum:
- process name
- purpose
- parameters
- prolog source
- metadata placeholders
- tags:
  - `IMF`
  - `Security`
  - environment scope if relevant

Ensure the `.json` structure is clean and deterministic so it can be versioned in Git.

---

## Quality constraints
- Use consistent IMF naming everywhere
- No hardcoded user names
- No direct granting to individuals
- Group-based design only
- Do not invent unsupported TM1 functions without clearly marking them as placeholders
- Prefer honest placeholders over pretending native security APIs exist
- Keep implementation compatible with Codex-driven repo workflows
- Make outputs easy to review in pull requests

---

## Output structure

Create:

src/
  ti_processes/
    IMF.P.Security.BootstrapAll.ti
    IMF.P.Security.BootstrapAll.json
    IMF.P.Security.CreateGroups.ti
    IMF.P.Security.CreateGroups.json
    IMF.P.Security.CreateSingleGroup.ti
    IMF.P.Security.CreateSingleGroup.json
    IMF.P.Security.ApplyModel.ti
    IMF.P.Security.ApplyModel.json
    IMF.P.Security.SetCubeAccess.ti
    IMF.P.Security.SetCubeAccess.json
    IMF.P.Security.SetDimensionAccess.ti
    IMF.P.Security.SetDimensionAccess.json
    IMF.P.Security.ExportProcessMatrix.ti
    IMF.P.Security.ExportProcessMatrix.json
    IMF.P.Security.ExportSecurityMatrix.ti
    IMF.P.Security.ExportSecurityMatrix.json
    IMF.P.Security.ValidateGroups.ti
    IMF.P.Security.ValidateGroups.json
    IMF.P.Security.ValidateObjectSecurity.ti
    IMF.P.Security.ValidateObjectSecurity.json
    IMF.P.Security.LogBootstrap.ti
    IMF.P.Security.LogBootstrap.json

docs/
  security/
    IMF_Security_Model.md
    IMF_Security_Matrix.csv
    IMF_Process_Security_Matrix.csv
    README.md

---

## Expected coding style
For each `.ti` file:
- start with a short header comment
- include parameter section
- include prolog only unless additional sections are needed
- keep code readable and structured
- mark every environment-specific implementation point with `TODO:`

For each `.json` file:
- mirror the `.ti` content
- include parameter definitions
- include process description
- include source text for prolog
- keep formatting stable for Git diffs

---

## Final step
After generating files:
1. summarize what was created
2. list all files
3. call out all `TODO` sections explicitly
4. identify any assumptions that depend on the target TM1 environment