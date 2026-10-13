# gunsnprices


Parse firearm and ammunition product titles into structured data: brand, model, caliber, magazine capacity, barrel length,
rounds per box and cost per round.

```python
>>> from gunsnprices import parse_title
>>> info = parse_title("Glock 19 Gen 5 MOS 9mm 4.02in 15rd Pistol PA195S203MOS")
>>> info.model.model, info.caliber.name, info.capacity, info.barrel_length
('Glock 19 Gen 5 MOS', '9×19mm Parabellum', 15, 4.02)
```

This is the title parser behind [GunsNPrices](https://gunsnprices.com), a price comparison site that tracks 40+ US gun
and ammo stores. Store titles are messy (`G19 GEN5 9MM 15RD FS`, `O/U 12/28 BL/WD 3"`, `Federal 308 150gr ... 20rds`),
and matching the same product across stores starts with reading them reliably. The model dictionaries and the caliber
list in this package are the ones the site uses to group listings, so you get the same model names you see on
gunsnprices.com.

No dependencies, pure Python 3.9+, about 1 ms per title.

## Install

```bash
pip install gunsnprices
```

A JavaScript version with the same API and the same test cases is on npm: `npm install gunsnprices`
([source](https://github.com/gunsnprices/gunsnprices-js)).

## What it recognizes

| Field | Example in a title | Result |
|---|---|---|
| Firearm or ammo | `... 150gr ... 20rds` | `kind="ammo"` |
| Brand and model (50 brands) | `G19 Gen5 MOS`, part number `PA195S203` | `Glock 19 Gen 5 MOS` |
| Calibers (293) | `.357 Mag / .38 Spl`, `6.5 CM`, `12ga`, `300 BLK`, `7MM RM` | `.357 Mag`, `.38 S&W Special`, ... |
| Magazine capacity | `15+1`, `17RD`, `13rd/15rd`, `10-shot` | `15`, `17`, `15`, `10` |
| Barrel length, inches | `4.02in`, `16 1/2"`, `22 BBL`, `O/U 12/28` | `4.02`, `16.5`, `22.0`, `28.0` |
| Rounds per box | `50/Box`, `Box of 20`, `1,000 Rounds`, `20/25` | `50`, `20`, `1000`, `20` |
| Cost per round | price `449.99` + `1000 Rounds` | `0.45` |

Brands with model dictionaries: Barrett, Benelli, Beretta, Bergara, Browning, Cadex, Canik, Charles Daly, Chiappa,
Christensen Arms, Cimarron, CMMG, Colt, CVA, CZ, Daniel Defense, Desert Eagle, Diamondback, Fierce, FN, Glock,
Great Lakes, Henry, Heritage, HK, Howa, Kel-Tec, Kimber, Kriss, Marlin, Mossberg, Remington, Retay, Rossi, Ruger, Savage,
SCCY, Seekins, Shadow Systems, Sig Sauer, Smith & Wesson, Springfield, Stevens, Stoeger, Taurus, Tikka, Tristar, Walther,
Weatherby, Winchester.

Next: [Usage](usage.md) · [Accuracy](accuracy.md) · [Data and license](data.md)
