
# Intito MasterFlow

Framework for version-controlled master data management in IBM Planning Analytics (TM1).

## Key Capabilities

- Versioned dimension changes
- Impact analysis before publish
- Automatic master archiving
- Rollback to previous versions
- Export/import integration
- Full audit trail

## Repository Structure

docs/        → architecture and design
src/         → TM1 objects and processes
tests/       → unit and integration tests
prompts/     → Codex prompts and runbooks

## Implementation

Follow the Codex runbook located in:

docs/architecture/codex_runbook.md

## Bedrock Design

Bedrock adoption design and the IMF refactor register are documented in:

- [IMF_Bedrock_Adoption_Design.md](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Adoption_Design.md)
- [IMF_Bedrock_Process_Mapping.csv](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Process_Mapping.csv)
- [IMF_Bedrock_Refactor_Register.yaml](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Bedrock_Refactor_Register.yaml)

## Release And Build Management

IMF release/build policy and templates are documented in:

- [IMF_Release_Build_Management.md](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Release_Build_Management.md)
- [docs/releases/README.md](/c:/Programming/Intito-Master-Flow/docs/releases/README.md)
- [imf-build-template.json](/c:/Programming/Intito-Master-Flow/build/manifests/imf-build-template.json)

Living status documents:

- [process_implementation_status.md](/c:/Programming/Intito-Master-Flow/docs/status/process_implementation_status.md)
- [bedrock_refactor_status.md](/c:/Programming/Intito-Master-Flow/docs/status/bedrock_refactor_status.md)
- [IMF_Remaining_Work_Plan.md](/c:/Programming/Intito-Master-Flow/docs/status/IMF_Remaining_Work_Plan.md)
- [release_status.md](/c:/Programming/Intito-Master-Flow/docs/status/release_status.md)

## Language Support

IMF language support design and governance are documented in:

- [IMF_Language_Support_Design.md](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Language_Support_Design.md)
- [IMF_Language_Governance.md](/c:/Programming/Intito-Master-Flow/docs/governance/IMF_Language_Governance.md)
- [IMF_Language_Key_Register.csv](/c:/Programming/Intito-Master-Flow/docs/architecture/IMF_Language_Key_Register.csv)
- [language_support_status.md](/c:/Programming/Intito-Master-Flow/docs/status/language_support_status.md)
