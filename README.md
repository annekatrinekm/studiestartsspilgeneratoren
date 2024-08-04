# Den aller sejeste studiestarsspils-generator
Copyright, owner and creator: Annekatrine Kirkterp-Møller

Scriptet her genererer en spilleplade med 69 (nice!) felter (inkl. START). Spillet er lavet til at blive printet i A0 og har dimensioner herefter (14043 × 9933px, 300dpi). Spillet eksporteres som en PNG. 

## Download
Download scriptet, fonten og CSV filen. 
Sørg for, at der er en mappe til alle billeder, i default hedder denne billede_mappe
Scriptet kræver PIL pakken, *pip install pillow*.

## Udfyld settings i starten af scriptet
Øverst i scriptet er en sektion med *settings*, som har de meste basale settings, herunder fil-navn for det færdige spil, default felt-baggrunds farve, navn på billede-mappen, og navnet på filen for regelsættet, der skal være i midten. 
### Regelsættet
Man skal selv lave billedet, som skal sidde i midten af spillet (hvor reglerne for spillet står). Billedet skal have ca. dimensionerne 1:1.06 da det bliver resizet til at passe i midten (4584x4323px). Denne fil skal være en jpg eller png. 

## Indtast data
CSV-filen skal udfyldes, som kort forklaret øverst i filen.
titel; billede_fil; billede_retning; felt_farve; tekst
Filen skal være er semi-colon (;) sepereret eller tab (\t) sepereret. Hvis den er tab-sepereret skal den have .tsv fil-endelse. Whitespaces ignoreres (ikke mellemrum i teksten dog). 
Linjer der starter med # ignoreres. 
### Start feltet
Start-feltet auto-genereres med teksten START på, i to farver, disse skrives i CSV'en på linjen der starter med 'Start-felt;'.
### Titler
Titler er valgfri. Titler bliver altid omdannet til all-caps på brættet.
### Billeder
Billeder er valgfri, hvis ikke de indsættes centreres teksten bare i feltet.
#### Billeder kan ikke være transparente PNG'er! 
Hvis et billede er indsat, så kan billedets retning angives. Man kan vælge imellem vandret eller lodret. Vandret er default, hvis intet angives. Hvis man har et billede i landsscape er det fordelagtigt at have det vandret og ligeledes, hvis man har et billede i portræt-format, kan det være bedre lodret. Generer evt. spillet med alle vandrette og se om nogle vil være bedre lodrette. 
### Felt farve
Feltets baggrundsfarve angives her. Farver kan angives som strings og man kan vælge imellem alle de gængse HTML farve-navne. Se f.eks. oversigt her: https://htmlcolorcodes.com/color-names/
