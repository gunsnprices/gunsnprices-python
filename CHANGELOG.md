# Changelog

## 0.1.0 (2026-10-12)

First release.

- `parse_title()`: firearm or ammo, brand, model, calibers, magazine capacity, barrel length, rounds per box, cost per round.
- `identify_model()`: 50 brands, the same model dictionaries that GunsNPrices uses on its site; decodes Glock part numbers.
- `find_calibers()` / `normalize_caliber()`: 293 calibers with retailer spellings.
- `magazine_capacity()`, `barrel_length()`, `rounds_per_box()`, `cost_per_round()`.
- Command line: `gunsnprices "title"` or `python -m gunsnprices`.
