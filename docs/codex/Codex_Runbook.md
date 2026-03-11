
# Codex runbook - full blueprint

## Steg 1
Skapa core metadata: dimensioner, cubes och namnstandard.

## Steg 2
Implementera versionsmotorn:
- IMF.P.Version.Create
- IMF.P.Version.CloneFromMaster
- IMF.P.Version.CloneFromVersion
- IMF.P.Version.Lock
- IMF.P.Version.Unlock

## Steg 3
Implementera copy/diff:
- IMF.P.Dimension.CopyAll
- IMF.P.Compare.VersionToMaster

## Steg 4
Implementera validering:
- IMF.P.Validate.Technical
- IMF.P.Validate.Business

## Steg 5
Implementera impact analysis:
- IMF.P.Impact.RunAll
- IMF.P.Impact.Cubes
- IMF.P.Impact.Subsets
- IMF.P.Impact.Views
- IMF.P.Impact.Processes
- IMF.P.Impact.Security
- IMF.P.Impact.Integrations

## Steg 6
Implementera publish, arkiv och rollback.

## Steg 7
Implementera export/import.

## Steg 8
Bygg PAW-bok och smoke tests.

## Steg 9
Aktivera deployment pipeline.

## Steg 10
Aktivera AI-governance och dokumentera beslut i ADR-filer.
