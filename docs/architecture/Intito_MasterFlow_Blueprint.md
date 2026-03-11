
# Intito MasterFlow Blueprint

## 1. Målbild
Intito MasterFlow är ett MDM-ramverk för IBM Planning Analytics / TM1 som gör det möjligt att hantera flera dimensioner genom versionerade arbetskopior, impact analysis, kontrollerad publicering, arkivering och rollback.

## 2. Lösningskomponenter
- Masterdimensioner
- Flera parallella arbetsversioner per dimension
- Arkivkopior av publicerade masterversioner
- Kontrollcubes för konfiguration, version, diff, validering, impact och audit
- TI-processbibliotek för copy, compare, validate, impact, publish, rollback, export/import
- PAW-bok för styrning och uppföljning
- Git-baserad deployment pipeline

## 3. Datamodell
Se `docs/object_catalog/Intito_MasterFlow_DataModel.xlsx`.

## 4. Impact analysis
Impact analysis körs före publish och rollback. Den använder diff som källa och analyserar påverkan på cubes, subsets, views, processer, säkerhet och integrationer.

## 5. PAW UI
PAW-boken består av flikarna:
- Översikt
- Versioner
- Redigering
- Validering
- Impact
- Publish
- Arkiv
- Rollback
- Export/Import

## 6. Deployment
Se `.github/workflows/tm1-deploy.yml`.

## 7. AI-assisterad governance
Se `docs/governance/AI_Masterdata_Governance.md`.
