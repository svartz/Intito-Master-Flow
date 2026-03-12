# PAW UI Design

## Language Support
PAW surfaces in IMF must distinguish between technical object names and display text.

Rules:
- technical names such as `IMF.P.*`, `IMF.C.*`, and `IMF.D.*` must not be translated
- tab names, instructions, status labels, and validation messages must be resolvable through IMF text keys
- default language is `en-US`
- fallback language is `en-US`
- supported languages are `en-US`, `sv-SE`, `fi-FI`, `sv-FI`, `no-NO`, `da-DK`, and `de-DE`

Implications:
- PAW design must use captions and text keys for user-facing text
- technical object names must only be shown where technical identification is required
- IMF should primarily use the `IMF.P.Text.ResolveWithFallback` pattern and `IMF.C.Text` to retrieve localized display text

## Tab 1 - Overview
Shows per dimension:
- active master
- number of open versions
- latest publish
- blockers
- latest impact status

Language rule:
- tab title and status labels must be localizable

## Tab 2 - Versions
Shows all work versions with status, created by, lock state, impact status, and approval.

Language rule:
- column headers and status values must be translatable

## Tab 3 - Editing
Opens the selected work version in the dimension editor and shows attributes and instructions.

Language rule:
- instructions and help text must come from the IMF text model

## Tab 4 - Validation
Summarizes technical errors, business rule violations, alias collisions, and missing mandatory attributes.

Language rule:
- validation messages must come from the IMF text model, not from hardcoded string literals
- initial keys exist for `validation.mandatory_attribute_missing` and `validation.alias_collision`

## Tab 5 - Impact
Shows the impact on cubes, subsets, views, processes, security, and integrations.

Language rule:
- severity labels and explanations must be localizable

## Tab 6 - Publish
Shows pre-publish checks, the archive name that will be created, and publish status.

Language rule:
- publish status and instructional text must be localizable
- release notes must show language coverage and fallback rules per build

## Tab 7 - Archive
Lists archived master versions and publish history.

Language rule:
- business-facing labels and descriptions must be localizable

## Tab 8 - Rollback
Shows archive version selection, analysis results, and restore actions.

Language rule:
- rollback warnings and instructions must be localizable

## Tab 9 - Export/Import
Shows format, shape, and target/source selection.

Language rule:
- format names may remain technically stable
- help text, instructions, and error messages must be translatable
