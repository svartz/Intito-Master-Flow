# IMF Language Governance

## Purpose
This document defines how language support in IMF is governed.

## Supported Locales

- `en-US`
- `sv-SE`
- `fi-FI`
- `sv-FI`
- `no-NO`
- `da-DK`
- `de-DE`

## Default And Fallback

- default locale: `en-US`
- fallback locale: `en-US`

## Governance Rules

1. Technical IMF object names must never be translated.
2. New locales must be approved explicitly.
3. Every user-facing text must use a stable text key.
4. Missing translations must be visible and reportable.
5. Release readiness must include translation coverage review.

## Translation Ownership

Recommended ownership split:

- architecture/team lead owns language model and key structure
- product or business owner approves user-facing wording
- implementation owner updates IMF text objects and exports

## Locale Policy

### `en-US`

- mandatory baseline locale
- required for every release

### `sv-SE`, `fi-FI`, `sv-FI`, `no-NO`, `da-DK`, `de-DE`

- supported when keys are approved and coverage is maintained
- partial translations must be visible in status tracking

## `sv-FI` Policy

`sv-FI` must only remain a separate locale if Finland-Swedish wording is intentionally supported.

If not:

- deprecate it
- map it operationally to `sv-SE`

## Key Management Rules

Text keys should:

- be stable
- be language-neutral
- be domain-grouped
- avoid technical-object renaming side effects

Recommended pattern:

- `domain.context.message_name`

Examples:

- `ui.publish.tab.title`
- `validation.alias_collision`
- `security.group_missing`

## Release Governance

Before release:

1. confirm locale list
2. confirm default and fallback
3. review missing translations
4. update status and release notes
5. update build manifest if language support changed

## Environment Rule

Recommended operating model:

- DEV: language keys and partial translations may evolve rapidly
- TEST: missing translations should be reported clearly
- PROD: required locales should meet approved release coverage
