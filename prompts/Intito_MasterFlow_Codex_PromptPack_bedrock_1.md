# Codex Task: IMF Bedrock Wave 1 Refactor

Implement the first executable Bedrock-backed refactor wave for Intito MasterFlow (IMF).

Use the existing IMF Bedrock design documents as the governing baseline:

- `docs/architecture/IMF_Bedrock_Adoption_Design.md`
- `docs/architecture/IMF_Bedrock_Process_Mapping.csv`
- `docs/architecture/IMF_Bedrock_Refactor_Register.yaml`
- `docs/status/bedrock_refactor_status.md`

## Goal

Move IMF from Bedrock design-only status to a practical Wave 1 implementation where the first utility-facade processes can delegate to Bedrock safely and transparently.

## Scope

Work only in the current repo layout:

- `src/processes/`
- `docs/architecture/`
- `docs/status/`
- `docs/releases/`
- `tests/unit/`
- `prompts/`

Do not reintroduce `src/tm1/processes/`.

## Wave 1 Targets

Refactor these IMF processes first:

- `IMF.P.Dimension.Create`
- `IMF.P.Dimension.Clear`
- `IMF.P.Dimension.CopyRelations`
- `IMF.P.Attribute.CopyDefinitions`
- `IMF.P.Security.CreateGroups`
- `IMF.P.Security.SetCubeAccess`
- `IMF.P.Security.SetDimensionAccess`
- `IMF.P.Log.Event`

## Required Rules

1. IMF processes remain the public entry points.
2. Do not rename IMF processes.
3. Add explicit Bedrock delegation only where the contract can be stated honestly.
4. Use opt-in delegation parameters such as:
   - `pUseBedrock`
   - `pBedrockProcess`
   - `pStrictBedrock`
5. Preserve native IMF fallback where safe.
6. Do not invent Bedrock parameter contracts without marking them as `TODO:`.
7. Log before and after Bedrock delegation where possible.
8. Keep IMF control-cube and governance ownership in IMF code.

## Implementation Expectations

### 1. Dimension utilities

For:

- `IMF.P.Dimension.Create`
- `IMF.P.Dimension.Clear`
- `IMF.P.Dimension.CopyRelations`

Implement:

- explicit Bedrock delegation path
- native fallback path where appropriate
- logging of delegation intent and fallback outcome
- parameterized Bedrock process name

Candidate processes:

- `}bedrock.dim.create`
- `}bedrock.dim.clone`
- `}bedrock.hier.clone`
- `}bedrock.hier.element.move`

### 2. Attribute utility

For:

- `IMF.P.Attribute.CopyDefinitions`

Implement:

- Bedrock-ready attribute-definition orchestration
- explicit contract checkpoints for attribute types and alias handling
- native fallback strategy or clearly documented TODO where type resolution is environment-specific

Candidate process:

- `}bedrock.dim.attr.create`

### 3. Security utilities

For:

- `IMF.P.Security.CreateGroups`
- `IMF.P.Security.SetCubeAccess`
- `IMF.P.Security.SetDimensionAccess`

Implement:

- Bedrock-backed group and object-security delegation path
- IMF-owned policy enforcement remains in the IMF process
- native fallback or clear TODO where the target environment owns IAM/security plumbing

Candidate processes:

- `}bedrock.security.group.create`
- `}bedrock.security.object.assign`

### 4. Logging utility

For:

- `IMF.P.Log.Event`

Implement:

- Bedrock-backed server log delegation
- native `LogOutput` fallback
- severity mapping that remains explicit and reviewable

Candidate process:

- `}bedrock.server.writetomessagelog`

## Documentation Updates

Update as needed:

- `docs/status/bedrock_refactor_status.md`
- `docs/architecture/IMF_Bedrock_Refactor_Register.yaml`
- `docs/releases/unreleased.md`

If behavior changes materially, also update:

- `docs/architecture/IMF_Bedrock_Adoption_Design.md`

## Tests

Add or update static tests so the repo verifies:

- process pair completeness
- Bedrock delegation parameters exist on Wave 1 processes
- Bedrock process names are explicit in source
- TODO markers remain where parameter contracts are still environment-dependent

## Final Output Contract

When finished, return:

1. summary of what was implemented
2. files changed
3. Wave 1 Bedrock processes updated
4. remaining Bedrock TODOs
5. assumptions about Bedrock process contracts and TM1 environment behavior
6. verification result
