# Codex Task: IMF Language Support Implementation

Implement Phase 1 of multilingual language support for Intito MasterFlow (IMF) in IBM Planning Analytics / TM1 v12.

The repository already contains the initial language support design, governance, status documentation, and first control-object definitions.

Your task is to move IMF language support from design-level definition to implementation-ready source and connected workflow behavior.

You must:

1. use the existing IMF naming and repository conventions
2. keep technical object names untranslated
3. implement translation-key driven language support
4. preserve Git-friendly deterministic source artifacts
5. remain honest where TM1 runtime or PAW behavior is environment-dependent

---

# Repository Layout

Use the existing repository layout exactly.

Current relevant paths include:

- `src/processes/`
- `src/object-definitions/`
- `docs/architecture/`
- `docs/governance/`
- `docs/status/`
- `docs/releases/`

Do not reintroduce `src/tm1/processes/`.

All new TI processes must be created under:

- `src/processes/`

All new object definitions must be created under:

- `src/object-definitions/`

---

# Existing Language Model

Use the already defined IMF language model.

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

Technical object names must never be translated:

- `IMF.P.*`
- `IMF.C.*`
- `IMF.D.*`

Use the existing documents as the governing design baseline:

- `docs/architecture/IMF_Language_Support_Design.md`
- `docs/governance/IMF_Language_Governance.md`
- `docs/status/language_support_status.md`
- `docs/architecture/IMF_Language_Key_Register.csv`

Use the existing control objects as the implementation baseline:

- `IMF.D.Language`
- `IMF.D.TextKey`
- `IMF.D.TextMeasure`
- `IMF.C.Text`

---

# Primary Objective

Implement the first usable IMF multilingual framework so that:

1. user-facing text can be resolved by text key and locale
2. fallback to `en-US` works consistently
3. language coverage can be validated and exported
4. PAW-facing and operator-facing text can be localized without changing technical object names
5. release/build artifacts can record language support status

---

# Required Implementation Areas

## 1. Text Resolution Engine

Implement a reusable process-based pattern for resolving text keys.

Required processes:

- `IMF.P.Text.Resolve`
- `IMF.P.Text.ResolveWithFallback`

Required behavior:

- accept text key and requested locale
- resolve text from `IMF.C.Text`
- fallback to `en-US`
- return explicit missing-text marker if translation is missing
- do not fake success for missing translations

Suggested missing marker:

- `[missing:<TextKey>]`

---

## 2. Translation Governance / Validation

Implement validation processes for language coverage.

Required processes:

- `IMF.P.Text.ValidateCoverage`
- `IMF.P.Text.ReportMissing`

Required behavior:

- validate required text keys
- validate `en-US` baseline coverage
- report missing translations for requested locales
- export deterministic coverage results
- support release readiness checks

Recommended output shape:

- `TextKey`
- `Domain`
- `Locale`
- `Required`
- `Status`
- `Comment`

---

## 3. Translation Import / Export

Implement maintainable translation interchange.

Required processes:

- `IMF.P.Text.Export`
- `IMF.P.Text.Import`

Required behavior:

- export `IMF.C.Text` content to deterministic file format
- import translation updates back into `IMF.C.Text`
- support at minimum CSV
- preserve stable text keys
- reject attempts to translate technical object names

---

## 4. Seed / Bootstrap Support

Implement bootstrap support for language control objects.

Required process:

- `IMF.P.Text.Init`

Required behavior:

- seed supported languages
- seed baseline text measures if missing
- seed initial text keys from the register where appropriate
- preserve existing data where possible

If actual seeding logic depends on deployment/runtime conventions:

- mark with explicit `TODO:`

---

## 5. PAW / UI Language Integration

Implement the first IMF-supported integration pattern for PAW-facing text.

Required behavior:

- document how PAW labels and instructions should resolve text keys
- do not translate technical object names
- separate business captions from technical identifiers
- support locale-driven captions for:
  - overview labels
  - validation labels
  - publish labels
  - rollback labels
  - import/export helper text

If direct runtime PAW localization depends on environment-specific setup:

- document the exact dependency
- use `TODO:` markers instead of inventing unsupported behavior

---

## 6. Validation / Security Message Localization

Introduce localized message handling for user-facing validation and security text.

Required behavior:

- identify the current hardcoded user-facing message locations
- convert at least the message model to text keys
- keep technical logs stable where localization is not appropriate
- make validation and security output localization-ready

Focus first on:

- validation messages
- security bootstrap messages
- audit/user-facing lifecycle messages

---

## 7. Release / Build Integration

Update release and build artifacts to track language support status.

Required behavior:

- ensure manifests record language support baseline
- ensure release notes include locale coverage
- ensure `unreleased.md` can track language support changes
- ensure status docs reflect current implementation maturity

---

# JSON Process Format

For every new process there must be:

- `<ProcessName>.ti`
- `<ProcessName>.json`

JSON must remain deterministic and Git-friendly.

Each JSON file must include at minimum:

- `Name`
- `name`
- `Purpose`
- `purpose`
- `Parameters`
- `parameters`
- `Prolog`
- `prolog`
- `Metadata`
- `metadata`
- `tags`
- `environmentScope`

Required tags:

- `IMF`
- `TM1`
- `PAW`
- `v12`
- `Language`

Add additional tags such as:

- `Validation`
- `Import`
- `Export`
- `UI`

where relevant.

---

# Coding Rules

Use consistent IMF naming.

Do not invent unsupported TM1 functions.

Do not translate technical object names.

Do not hardcode user names.

Do not fake native multilingual behavior where the environment does not support it.

Where environment-specific behavior is required:

- mark it as `TODO:`
- validate around it
- document it clearly

Prefer:

- text keys
- deterministic exports
- explicit fallback handling
- narrow, honest assumptions

---

# Verification Requirements

Before finishing:

1. confirm all new language-support processes have both `.ti` and `.json`
2. confirm all JSON contracts are complete
3. confirm `IMF.C.Text` and related dimensions are consistent with the design
4. confirm release/build docs reflect language support
5. confirm no technical object names are being translated
6. confirm missing translations are reportable

If tests exist, extend them where needed.

At minimum, add or update coverage for:

- text resolution
- fallback behavior
- missing-translation reporting
- process pair consistency

---

# Documentation Updates

Update related documentation if implementation changes behavior.

At minimum review and update if needed:

- `docs/architecture/IMF_Language_Support_Design.md`
- `docs/governance/IMF_Language_Governance.md`
- `docs/status/language_support_status.md`
- `docs/architecture/PAW_UI_Design.md`
- `docs/releases/unreleased.md`

---

# Final Output Contract

When done, return:

## 1. Summary
A concise summary of what was implemented.

## 2. Files changed
List every file created or modified.

## 3. Processes completed
List all new or updated language-support processes.

## 4. Remaining TODOs
List only genuinely environment-dependent localization TODOs.

## 5. Assumptions
List assumptions about:

- TM1 v12 runtime behavior
- PAW localization behavior
- prompt localization limitations
- locale governance
- release/build integration

## 6. Verification result
State whether:

- process pairs are complete
- language control objects are defined
- fallback behavior is connected
- blockers remain
