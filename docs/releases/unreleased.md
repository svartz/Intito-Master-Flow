# Unreleased

## Added

- Placeholder for newly added IMF processes, objects, tests, and documentation.
- Initial language support architecture, governance, status, key register, and control-object design.
- Phase 1 language support processes: `IMF.P.Text.Resolve`, `IMF.P.Text.ResolveWithFallback`, `IMF.P.Text.ValidateCoverage`, `IMF.P.Text.ReportMissing`, `IMF.P.Text.Export`, `IMF.P.Text.Import`, and `IMF.P.Text.Init`.
- Static test coverage for language process pairs, fallback marker behavior, and text-key seeding.
- Static test coverage for Wave 1 Bedrock facade parameters and source markers.
- Source-controlled PAW workbook specifications for `IMF.PAW.MasterFlow`.

## Changed

- Placeholder for behavior changes in existing IMF process flows.
- `IMF.D.TextKey` now seeds the current language key register baseline.
- Language support status and PAW UI design now reflect the implemented text-resolution workflow.
- `IMF.P.Dimension.Create` and `IMF.P.Log.Event` now support opt-in Bedrock delegation with native fallback.
- `IMF.P.Dimension.CopyRelations` now performs native element and relation replay when Bedrock delegation is not used or fails.
- `IMF.P.Attribute.CopyDefinitions` now includes Bedrock-ready orchestration and explicit Bedrock contract checkpoints.
- `IMF.P.Attribute.CopyValues` now performs native attribute-value replay for matching target elements.
- `IMF.P.Compare.VersionToMaster`, `IMF.P.Compare.Elements`, `IMF.P.Compare.Relations`, and `IMF.P.Compare.Attributes` now write baseline diff records to `IMF.C.Diff`.
- `IMF.P.Commit.ArchiveMaster` now creates and populates an archive dimension before publish.
- `IMF.P.Commit.PublishVersion` now replaces the master dimension from the work version after archive creation.
- `IMF.P.Rollback.Validate` and `IMF.P.Rollback.ToArchive` now perform baseline restore validation and master backup before rollback.
- `IMF.P.Dimension.Clear`, `IMF.P.Dimension.CopyRelations`, `IMF.P.Security.CreateGroups`, `IMF.P.Security.SetCubeAccess`, and `IMF.P.Security.SetDimensionAccess` now include Wave 1 Bedrock delegation parameters and documented contract boundaries.

## Fixed

- Placeholder for defect fixes in IMF logic, deployment, or documentation.

## Known Issues

- Placeholder for issues still present before the next release.

## Release Readiness Checklist

- [ ] `tools/tm1_deploy.py validate` passes
- [ ] process and object documentation updated where needed
- [ ] build manifest prepared
- [ ] release note prepared
- [ ] tag name decided
