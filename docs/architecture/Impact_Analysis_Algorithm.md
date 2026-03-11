
# Impact analysis - algoritm för TM1

## Input
- IMF.C.Diff
- IMF.C.Version
- IMF.C.Config

## Pseudokod
1. Läs diff för vald version
2. Klassificera ändringar: add, delete, move, attribute, alias, relation
3. Hitta berörda cubes via dimensionsreferenser
4. Hitta berörda subsets och views
5. Skanna TI-processer efter beroenden till element, attributes, subsets och dimensioner
6. Kontrollera påverkan på security-objekt
7. Kontrollera integrationskontrakt:
   - leaf key ändrad
   - full path ändrad
   - attribut som används i export ändrade
8. Beräkna business impact:
   - antal leafs flyttade
   - antal deletes
   - antal nya element
   - antal ändrade attribut
9. Tilldela severity:
   - Info
   - Warning
   - Error
   - Blocker
10. Summera blockerare och skriv status:
   - ImpactAnalyzed om blockerare = 0
   - Blocked om blockerare > 0

## Publiceringsregel
Publish får endast ske om:
- teknisk validering = godkänd
- impact analysis = körd
- blockerare = 0
- eventuell approval = klar
