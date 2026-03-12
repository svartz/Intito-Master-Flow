# IMF Language Support Status

## Current Model

- Supported locales:
  - `en-US`
  - `sv-SE`
  - `fi-FI`
  - `sv-FI`
  - `no-NO`
  - `da-DK`
  - `de-DE`
- Default locale: `en-US`
- Fallback locale: `en-US`

## Current Assessment

| Area | Status | Notes |
|---|---|---|
| Language design | defined | Initial architecture and governance documents created. |
| Translation control objects | defined | First object definitions proposed in `src/object-definitions`. |
| Text key register | started | Initial key register added. |
| PAW-facing language model | partial | UI document updated with localization principles. |
| TI message localization | not started | Existing processes still mostly use hardcoded or placeholder text. |
| Process prompt localization | environment-dependent | Depends on runtime/UI resolution strategy. |
| Release traceability | partial | Build template and release docs now need language fields populated in real releases. |

## Known Risks

- `sv-FI` may add maintenance cost if not genuinely needed.
- Always-fallback-to-English is operationally safe but may not be ideal UX for all Nordic users.
- Native TI prompt localization is not guaranteed without a wrapper or UI layer.

## Next Steps

1. decide whether `sv-FI` remains a first-class locale
2. implement `IMF.D.Language`, `IMF.D.TextKey`, `IMF.D.TextMeasure`, and `IMF.C.Text`
3. start with validation and security message keys
4. add release coverage reporting for translations
