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
| Translation control objects | implementation-ready | Control objects are defined and the text key dimension now seeds the current register baseline. |
| Text key register | connected | The current register keys are mirrored in `IMF.D.TextKey` and seeded by `IMF.P.Text.Init`. |
| PAW-facing language model | partial | UI document updated with localization principles. |
| TI message localization | partial | `IMF.P.Text.Resolve*`, coverage, export, and bootstrap processes are now in source control. |
| Process prompt localization | environment-dependent | Depends on runtime/UI resolution strategy. |
| Release traceability | connected | Release/build templates now reference locale coverage and the language processes can export deterministic reports. |

## Known Risks

- `sv-FI` may add maintenance cost if not genuinely needed.
- Always-fallback-to-English is operationally safe but may not be ideal UX for all Nordic users.
- Native TI prompt localization is not guaranteed without a wrapper or UI layer.

## Next Steps

1. decide whether `sv-FI` remains a first-class locale
2. wire `IMF.P.Text.Import` to a deployed TM1 datasource contract
3. replace hardcoded validation and security literals in the main IMF process library with text keys
4. add release coverage reporting for translations from deployed environments
