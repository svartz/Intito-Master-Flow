# PAW UI-design

## Sprakstod
PAW-ytor i IMF ska skilja mellan tekniska objektnamn och visningstext.

Regler:
- tekniska namn som `IMF.P.*`, `IMF.C.*` och `IMF.D.*` oversatts inte
- fliknamn, instruktioner, statusetiketter och valideringsmeddelanden ska kunna resolveas via IMF:s spraknycklar
- default-sprak ar `en-US`
- fallback-sprak ar `en-US`
- stodda sprak ar `en-US`, `sv-SE`, `fi-FI`, `sv-FI`, `no-NO`, `da-DK`, `de-DE`

Konsekvens:
- PAW-designen ska anvanda captions och textnycklar for anvandartext
- tekniska objektnamn ska endast visas dar teknisk identifiering behovs

## Flik 1 - Oversikt
Visar per dimension:
- aktiv master
- antal oppna versioner
- senaste publish
- blockerare
- senaste impact-status

Sprakregel:
- tabtitel och statusetiketter ska vara lokaliserbara

## Flik 2 - Versioner
Visar samtliga arbetsversioner med status, skapad av, las, impact-status och approval.

Sprakregel:
- kolumnrubriker och statusvarden ska kunna oversattas

## Flik 3 - Redigering
Oppnar vald arbetsversion i dimension editor och visar attribut och instruktioner.

Sprakregel:
- instruktioner och hjalptexter ska komma fran IMF:s textmodell

## Flik 4 - Validering
Summerar tekniska fel, affarsregelbrott, aliaskrockar och saknade obligatoriska attribut.

Sprakregel:
- valideringsmeddelanden ska komma fran IMF:s textmodell, inte hardkodade literalstrangar

## Flik 5 - Impact
Visar paverkan pa cubes, subsets, views, processer, sakerhet och integrationer.

Sprakregel:
- severity-etiketter och forklaringar ska kunna lokaliseras

## Flik 6 - Publish
Visar forhandskontroll, arkivnamn som kommer att skapas och publish-status.

Sprakregel:
- publish-status och instruktionstext ska kunna lokaliseras

## Flik 7 - Arkiv
Lista over arkiverade masterversioner och publiceringshistorik.

Sprakregel:
- affarsvanda listetiketter och beskrivningar ska kunna lokaliseras

## Flik 8 - Rollback
Val av arkivversion, analysresultat och aterstallning.

Sprakregel:
- rollback-varningar och instruktioner ska kunna lokaliseras

## Flik 9 - Export/Import
Val av format, shape och target/source.

Sprakregel:
- formatnamn kan vara tekniskt stabila
- hjalptexter, instruktioner och felmeddelanden ska kunna oversattas
