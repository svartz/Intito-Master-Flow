# AI-Assisted Master Data Governance

## Principle
AI is used as decision support, not as the decision-maker, in matters related to master data. All AI-generated suggestions must be traceable and reviewable.

## Use Cases
- proposals for validation rules
- proposals for mappings between import fields and attributes
- summaries of impact analysis results
- generation of test cases
- support for release notes and change descriptions

## Controls
- all AI-generated artifacts must be versioned in Git
- no master data changes may be published without human approval
- AI must never write directly to the master dimension
- prompts and responses that affect design or code must be stored in the repository

## Operating Model
1. AI proposes
2. A developer reviews
3. Code and tests are generated
4. Technical review is completed
5. Deployment runs through the pipeline
6. The audit trail is stored in MasterFlow
