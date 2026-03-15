# IMF Language Support Design

## Purpose
This document defines how language support in IMF should be specified, governed, documented, and implemented.

The goal is to make language support:

- predictable
- release-traceable
- implementation-friendly
- independent from technical object names

## Recommended Language Scope

Supported locales:

- `en-US`
- `sv-SE`
- `fi-FI`
- `sv-FI`
- `no-NO`
- `da-DK`
- `de-DE`

Default locale:

- `en-US`

Fallback locale:

- always `en-US`

## Evaluation Of The Proposed Model

The proposed language model is viable, but there are several important constraints.

### 1. `sv-FI` Requires Explicit Governance
`sv-FI` is a valid and useful business locale, but it introduces a semantic question:

- should Swedish in Finland be translated independently from Swedish in Sweden?

If yes:

- `sv-FI` must be treated as a first-class locale
- translation ownership and review must be explicit

If no:

- `sv-FI` should not exist as its own locale
- it should map to `sv-SE`

Recommendation:

- keep `sv-FI` only if there is a real UI or business requirement for Finland-Swedish wording

### 2. Global Fallback To `en-US` Is Safe But Not Always Ideal
Always falling back to English is technically simple and operationally safe.

Potential downside:

- Nordic users may prefer same-language regional fallback before English

Examples:

- `sv-FI` could reasonably fall back to `sv-SE`
- `no-NO` and `da-DK` may sometimes be better served by English than cross-Nordic fallback

Recommendation:

- phase 1: global fallback to `en-US`
- future option: per-locale fallback chain

### 3. Cubes And Dimensions Must Be Distinguished From Their Labels
Technical objects should not be translated:

- `IMF.P.*`
- `IMF.C.*`
- `IMF.D.*`

That is correct and should remain mandatory.

What should be translated instead:

- captions
- display labels
- descriptions
- help text

Recommendation:

- treat object names as stable keys
- translate only presentation text

### 4. Process Prompts Need Special Handling
TI process prompts are not automatically multilingual in TM1 just because IMF stores translations in a cube.

This means:

- multilingual prompt display may depend on deployment/runtime conventions
- some prompts may remain English in native TM1 unless a wrapper or PAW UI resolves text dynamically

Recommendation:

- classify process prompts as supported, but document them as environment-dependent

### 5. Views And Subsets Need Presentation Scope Clarification
The requirement says subsets/views must be multilingual.

That is reasonable, but it must be clarified whether this means:

- object names remain technical, while titles/descriptions are translated
- or separate business-facing captions are maintained outside the technical subset/view name

Recommendation:

- do not translate technical subset/view object names
- translate display metadata only

### 6. Validation And Security Messages Should Use Text Keys
This is the most important implementation rule.

Do not hardcode user-facing messages directly in TI where language support is required.

Use:

- text keys
- a central translation store
- deterministic fallback rules

## Language Support Scope In IMF

The following must be multilingual:

- cube captions and descriptions
- dimension captions and descriptions
- element labels where business-facing
- business-facing attributes and attribute descriptions
- subset and view captions/descriptions
- process prompts where runtime supports localized presentation
- validation messages
- security and audit messages intended for users or operators
- PAW-facing labels and instructional text

The following must not be translated:

- technical object names
- process identifiers
- cube names
- dimension names
- control-object identifiers
- key values used for joins, lookups, or deployment

## Implementation Model

Language support in IMF should be implemented through dedicated control objects.

### Dimensions

- `IMF.D.Language`
- `IMF.D.TextKey`
- `IMF.D.TextMeasure`

### Cube

- `IMF.C.Text`

Recommended `IMF.C.Text` grain:

- `TextKey`
- `Language`
- `Measure`

Recommended measures:

- `Text`
- `Status`
- `Domain`
- `Owner`
- `LastUpdatedBy`
- `LastUpdatedAt`

## Translation Key Model

User-facing text should be identified by stable keys.

Examples:

- `ui.overview.tab.title`
- `validation.mandatory_attribute_missing`
- `security.bootstrap.started`
- `impact.blocker_detected`

Rules:

1. keys are language-neutral
2. keys are stable across releases unless meaning changes materially
3. technical object names are not used as translated display text

## Suggested Translation Domains

- `UI`
- `Validation`
- `Security`
- `Audit`
- `Workflow`
- `Help`
- `Metadata`

## Fallback Rules

Phase 1 fallback:

1. requested locale
2. `en-US`
3. key itself or explicit missing-text marker

Recommended missing text marker:

- `[missing:<TextKey>]`

## Process Design Rules

When a TI process needs user-facing text:

1. resolve locale
2. resolve text key
3. read translated text from `IMF.C.Text`
4. fallback to `en-US`
5. only then emit to UI, audit, validation, or export

Phase 1 implementation-ready process set:

- `IMF.P.Text.Resolve`
- `IMF.P.Text.ResolveWithFallback`
- `IMF.P.Text.ValidateCoverage`
- `IMF.P.Text.ReportMissing`
- `IMF.P.Text.Export`
- `IMF.P.Text.Import`
- `IMF.P.Text.Init`

Current implementation note:

- text resolution, fallback, coverage reporting, export, and bootstrap seeding are implemented in source
- CSV import is intentionally left as an honest datasource-wiring TODO because the deployed TM1 datasource convention is environment-specific

## PAW Design Implications

PAW design should use translated labels, not technical object names, for:

- page labels
- section labels
- instructional text
- user-facing status text

The PAW UI design should explicitly distinguish:

- technical object name
- business caption

## Governance Model

Language additions and translation lifecycle are governed in:

- [IMF_Language_Governance.md](/c:/Git/Intito-Master-Flow/docs/governance/IMF_Language_Governance.md)

Status tracking is maintained in:

- [language_support_status.md](/c:/Git/Intito-Master-Flow/docs/status/language_support_status.md)

Key inventory is maintained in:

- [IMF_Language_Key_Register.csv](/c:/Git/Intito-Master-Flow/docs/architecture/IMF_Language_Key_Register.csv)

## Release And Build Traceability

Each release should record:

- supported locales
- default locale
- fallback rule
- translation coverage status
- open localization blockers

This should be reflected in:

- build manifest
- release notes
- language support status
- deterministic CSV outputs from `IMF.P.Text.ValidateCoverage` and `IMF.P.Text.ReportMissing`

## Decision

IMF should implement multilingual support through stable text keys and dedicated translation control objects, with:

- `en-US` as default
- `en-US` as mandatory fallback
- technical names kept untranslated
- language coverage tracked as part of release management
