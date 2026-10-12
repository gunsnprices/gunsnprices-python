# gunsnprices

[![PyPI](https://img.shields.io/pypi/v/gunsnprices)](https://pypi.org/project/gunsnprices/)
[![Python](https://img.shields.io/pypi/pyversions/gunsnprices)](https://pypi.org/project/gunsnprices/)
[![Tests](https://github.com/gunsnprices/gunsnprices-python/actions/workflows/ci.yml/badge.svg)](https://github.com/gunsnprices/gunsnprices-python/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY%204.0%20data-blue)](#license)

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

## Usage

### Everything at once

```python
from gunsnprices import parse_title

info = parse_title("Federal American Eagle 5.56x45mm 55gr FMJ 1000 Rounds", price=449.99)
info.kind              # 'ammo'
info.caliber.name      # '5.56×45mm NATO'
info.rounds            # 1000
info.cost_per_round    # 0.45

info.to_dict()         # plain dict, ready for json.dumps
```

`parse_title(title, brand=None, mpn="", sku="", price=None, kind=None)` returns a `ProductInfo`:

| Attribute | Type | Notes |
|---|---|---|
| `kind` | `str` | `"firearm"` or `"ammo"`; pass `kind=` to skip the guess |
| `brand` | `str` | brand of the identified model, else the `brand` you passed |
| `model` | `ModelMatch` or `None` | firearms only |
| `caliber` | `Caliber` or `None` | first caliber in the title |
| `calibers` | `list[Caliber]` | all calibers, in order |
| `capacity` | `int` or `None` | magazine capacity (for `15+1` it is 15), firearms only |
| `barrel_length` | `float` or `None` | inches, firearms only |
| `rounds` | `int` or `None` | rounds per box, ammo only |
| `cost_per_round` | `float` or `None` | ammo with `price` only |

Passing `brand` (the manufacturer field from a feed) helps with titles that don't name the brand. Passing `mpn` lets it
decode Glock part numbers when the title says nothing useful:

```python
>>> from gunsnprices import identify_model
>>> identify_model("GLOCK 9MM PISTOL 15RD", brand="Glock", mpn="UA4350201")
ModelMatch(brand='Glock', family='Glock 43', model='Glock 43', generation='', configs=[], features=[], source='mpn')
```

### Models

```python
from gunsnprices import identify_model, list_brands

m = identify_model("Sig Sauer P365 XL 9mm 3.7\" 12+1 Optic Ready")
m.brand, m.family, m.model    # ('Sig Sauer', 'Sig Sauer P365', 'Sig Sauer P365 XL')
```

`ModelMatch` has `brand`, `family`, `model` (the most specific name), `generation`, `configs` (such as `MOS`,
`Compact`), `features` (such as `Threaded Barrel`, `FDE`) and `source` (`"title"` or `"mpn"`). Accessories, parts,
airguns and airsoft are rejected, so it returns `None` for "Glock 19 holster" and "Umarex Glock 19 CO2 BB pistol".

### Calibers

```python
from gunsnprices import find_calibers, normalize_caliber, list_calibers

[c.name for c in find_calibers("Henry Big Boy .44 Mag/.44 Spl 20in")]
# ['.44 Magnum', '.44 S&W Special']

normalize_caliber("308 WIN (7.62X51 NATO)")
# Caliber(id='308win', name='.308 Win', type='rifle', url='https://gunsnprices.com/ammo/rifle-ammo/308-win')
```

Each `Caliber` has a stable `id`, a display `name`, a `type` (`handgun`, `rifle`, `rimfire`, `shotgun`, `airgun`,
`muzzleloader`) and the `url` of its GunsNPrices price comparison page. `normalize_caliber` is meant for caliber fields
in product feeds; `find_calibers` searches free text.

### Numbers

```python
from gunsnprices import magazine_capacity, barrel_length, rounds_per_box, cost_per_round

magazine_capacity("Springfield Hellcat Pro OSP 9mm 3.7in 15rd/17rd")   # 17
barrel_length('Mossberg 590 Persuader 12/20 BL/SY 3"')                # 20.0 (3" is the chamber)
rounds_per_box("Winchester 308 150gr PowerMax Bonded 20rds")           # 20
cost_per_round(31.99, 20)                                              # 1.5995
```

### Command line

```bash
$ gunsnprices "Ruger GP100 .357 Mag / .38 Special 4.2in 6-shot Revolver"
$ cat titles.txt | gunsnprices > parsed.jsonl
$ gunsnprices --price 18.99 "Federal 9mm 115gr FMJ 50/Box"
```

## Accuracy

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

## Data

The model dictionaries and caliber list ship inside the package (`gunsnprices/data/`). The same data, with listing
counts and price levels, is published as open datasets:

- Hugging Face: [gunsnprices/firearm-calibers](https://huggingface.co/datasets/gunsnprices/firearm-calibers),
  [gunsnprices/firearm-models](https://huggingface.co/datasets/gunsnprices/firearm-models)
- GitHub: [gunsnprices/firearm-datasets](https://github.com/gunsnprices/firearm-datasets)
- Kaggle: [gunsnprices](https://www.kaggle.com/gunsnprices)

## Limitations

- Titles from US retailers, in English.
- Models are covered for the 50 brands above. Other brands still get calibers and numbers.
- Built for firearms and ammunition. Magazines, parts and accessories get calibers and numbers but no model.

## License

The code is under the [MIT License](LICENSE). The data files in `gunsnprices/data/` are under
[CC BY 4.0](LICENSE-DATA): you can use them for anything, including commercial use, if you credit
**GunsNPrices (gunsnprices.com)** with a link.

Questions, corrections and missing models: open an issue or write to app@gunsnprices.com.
Current gun and ammo prices: [gunsnprices.com](https://gunsnprices.com).
