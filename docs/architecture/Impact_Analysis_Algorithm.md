# Impact Analysis Algorithm for TM1

## Inputs
- `IMF.C.Diff`
- `IMF.C.Version`
- `IMF.C.Config`

## Pseudocode
1. Read the diff for the selected version.
2. Classify changes as add, delete, move, attribute, alias, or relation changes.
3. Identify affected cubes from dimension references.
4. Identify affected subsets and views.
5. Scan TI processes for dependencies on elements, attributes, subsets, and dimensions.
6. Check the impact on security objects.
7. Check integration contracts:
   - leaf key changed
   - full path changed
   - attributes used in exports changed
8. Calculate business impact:
   - number of moved leaves
   - number of deletes
   - number of new elements
   - number of changed attributes
9. Assign severity:
   - `Info`
   - `Warning`
   - `Error`
   - `Blocker`
10. Summarize blockers and write status:
   - `ImpactAnalyzed` when blockers = 0
   - `Blocked` when blockers > 0

## Publish Rule
Publish is allowed only when:
- technical validation = approved
- impact analysis = completed
- blockers = 0
- any required approval = completed
