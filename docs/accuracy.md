# Accuracy

Measured on 50,202 firearm and 13,555 ammunition listings from 40+ stores on gunsnprices.com (October 2026),
against the attributes stored on the site:

| What | Found in the title | Right when found |
|---|---|---|
| Model (32,317 listings with a known model) | 99.97% | 99.8% same name as the site* |
| Caliber, firearms | 81% | 97.8% |
| Caliber, ammo | 91% | 94.9% |
| Magazine capacity | 46% | 95.6% |
| Barrel length | 58% | 94.4% |
| Rounds per box | 80% | 96.6% |

"Found" is limited by the titles themselves: many stores don't put the caliber or barrel length in the title at all.
Most of the "wrong" cases we checked by hand are errors in the store data, not in the parser: a 6mm Creedmoor rifle
labeled 6.5 Creedmoor, a "1000 Rounds" case stored as a box of 20.

\* The other 0.2% are the same model with a cleaner name: the site calls 52 listings "S&W M&P Shield Plus Plus Shield",
the library says "S&W M&P Shield Plus".
