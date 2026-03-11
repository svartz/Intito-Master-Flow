
# AI-assisterad masterdata governance

## Princip
AI används som stöd, inte som beslutsmotor, i frågor som rör masterdata. Alla AI-förslag måste vara spårbara och granskningsbara.

## Användningsfall
- förslag på valideringsregler
- förslag på mappings mellan importfält och attribut
- sammanfattning av impact analysis
- generering av testfall
- stöd till release notes och ändringsbeskrivningar

## Kontroller
- alla AI-genererade artefakter ska versioneras i Git
- inga masterändringar får publiceras utan mänsklig approval
- AI får aldrig skriva direkt till masterdimension
- prompts och svar som påverkar design eller kod ska sparas i repo

## Driftmodell
1. AI föreslår
2. Utvecklare granskar
3. Kod/test genereras
4. Teknisk review
5. Deployment via pipeline
6. Audit trail lagras i MasterFlow
