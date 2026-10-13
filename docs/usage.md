# Usage

## Everything at once

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

## Models

```python
from gunsnprices import identify_model, list_brands

m = identify_model("Sig Sauer P365 XL 9mm 3.7\" 12+1 Optic Ready")
m.brand, m.family, m.model    # ('Sig Sauer', 'Sig Sauer P365', 'Sig Sauer P365 XL')
```

`ModelMatch` has `brand`, `family`, `model` (the most specific name), `generation`, `configs` (such as `MOS`,
`Compact`), `features` (such as `Threaded Barrel`, `FDE`) and `source` (`"title"` or `"mpn"`). Accessories, parts,
airguns and airsoft are rejected, so it returns `None` for "Glock 19 holster" and "Umarex Glock 19 CO2 BB pistol".

## Calibers

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

## Numbers

```python
from gunsnprices import magazine_capacity, barrel_length, rounds_per_box, cost_per_round

magazine_capacity("Springfield Hellcat Pro OSP 9mm 3.7in 15rd/17rd")   # 17
barrel_length('Mossberg 590 Persuader 12/20 BL/SY 3"')                # 20.0 (3" is the chamber)
rounds_per_box("Winchester 308 150gr PowerMax Bonded 20rds")           # 20
cost_per_round(31.99, 20)                                              # 1.5995
```

## Command line

```bash
$ gunsnprices "Ruger GP100 .357 Mag / .38 Special 4.2in 6-shot Revolver"
$ cat titles.txt | gunsnprices > parsed.jsonl
$ gunsnprices --price 18.99 "Federal 9mm 115gr FMJ 50/Box"
```
