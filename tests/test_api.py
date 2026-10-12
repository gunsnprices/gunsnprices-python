import json

import pytest

import gunsnprices as g
from gunsnprices.__main__ import main


@pytest.mark.parametrize("title,brand,mpn,model", [
    ("Glock 19 Gen 5 MOS 9mm 4.02in 15rd Pistol", None, "", "Glock 19 Gen 5 MOS"),
    ("G19 Gen5 9mm 15rd FS", "Glock", "", "Glock 19 Gen 5"),
    ("Glock 43X 9mm 3.41in 10rd Black", None, "", "Glock 43X"),
    ("GLOCK 9MM PISTOL 15RD", "Glock", "PA195S203", "Glock 19 Gen 5"),
    ("Sig Sauer P365 XL 9mm 3.7in 12rd Pistol", None, "", "Sig Sauer P365 XL"),
    ("Ruger GP100 .357 Mag 4.2in 6rd Revolver", None, "", "Ruger GP100"),
])
def test_identify_model(title, brand, mpn, model):
    m = g.identify_model(title, brand=brand, mpn=mpn)
    assert m is not None and m.model == model


def test_identify_model_rejects_airguns_accessories_and_unknown():
    assert g.identify_model("Umarex Glock 19 CO2 BB Pistol .177") is None
    assert g.identify_model("Hornady 9mm 115gr FTX Critical Defense 25rd") is None
    assert g.identify_model("Glock 19 holster") is None
    assert g.identify_model("Sig P365 XL 12rd Magazine 9mm") is None
    assert g.identify_model("Magpul PMAG for Glock 19") is None
    assert g.identify_model("") is None


def test_included_accessories_keep_the_gun():
    assert g.identify_model("Glock 19 Gen 5 9mm 15rd w/ 3 magazines").model == "Glock 19 Gen 5"
    assert g.identify_model("Daniel Defense DDM4 V7 (No Magazine)") is not None


def test_mpn_source():
    m = g.identify_model("GLOCK 9MM PISTOL 15RD", brand="Glock", mpn="PA195S203")
    assert m.source == "mpn" and m.family == "Glock 19"


@pytest.mark.parametrize("text,names", [
    ("Ruger GP100 .357 Mag / .38 Special 4.2in Revolver", [".357 Mag", ".38 S&W Special"]),
    ("Federal American Eagle 9mm Luger 115gr FMJ 50rd", ["9×19mm Parabellum"]),
    ("Hornady 6.5 Creedmoor 143gr ELD-X", ["6.5mm Creedmoor"]),
    ("PSA AR-15 300 Blackout 16in Rifle", [".300 AAC Blackout"]),
    ("Kent 12G Fasteel 3in BBB", ["12 Gauge"]),
    ("Beretta 686 O/U 12/28 BL/WD 3\"", ["12 Gauge"]),
    ("Winchester 308 150gr PowerMax Bonded 20rds", [".308 Win"]),
    ("Remington 7mm RM 26\" Bolt Rifle", ["7mm Remington Magnum"]),
    ("Model 1911 Range Officer Parkerized", []),
])
def test_find_calibers(text, names):
    assert [c.name for c in g.find_calibers(text)] == names


def test_co2_cartridge_is_not_a_gauge():
    assert g.find_calibers("Umarex 12g CO2 Cartridges 15 pack") == []


def test_normalize_caliber():
    assert g.normalize_caliber("9mm Luger").id == "9x19mmparabellum"
    assert g.normalize_caliber("5.56 NATO").id == "5-56x45mmnato"
    assert g.normalize_caliber("12 GA").name == "12 Gauge"
    assert g.normalize_caliber("nothing here") is None


def test_lists():
    assert len(g.list_brands()) == 50 and "Glock" in g.list_brands()
    cals = g.list_calibers()
    assert len(cals) > 250 and len({c.id for c in cals}) == len(cals)


@pytest.mark.parametrize("title,cap", [
    ("Glock 19 Gen5 9mm 4.02in 15+1", 15),
    ("Kimber CDS9 9mm 3.18in 13rd/15rd Black", 15),
    ("Savage 110 Scout 450 Bushmaster 4 Round Bolt Action", 4),
    ("Ruger 10/22 Carbine 22LR", None),
])
def test_magazine_capacity(title, cap):
    assert g.magazine_capacity(title) == cap


@pytest.mark.parametrize("title,inches", [
    ('Ruger GP100 .357 Mag 4.2in Revolver', 4.2),
    ('Beretta A300 Ultima 12 GA 3" Chamber 28" Barrel', 28.0),
    ('Mossberg 590 Persuader 12/20 BL/SY 3"', 20.0),
    ('Colt Python 4 1/4" .357', 4.25),
    ('Ruger 10/22 SBR 22LR 8in 15rd', 8.0),
    ('Bergara B-14 24" 1:8" twist', 24.0),
    ('Glock 19 Gen5 9mm', None),
])
def test_barrel_length(title, inches):
    assert g.barrel_length(title) == inches


@pytest.mark.parametrize("title,n", [
    ("Federal American Eagle 9mm 115gr FMJ, 50/Box", 50),
    ("Prvi Partizan 5.56x45mm M193 55gr 1,000 Rounds", 1000),
    ("Lapua 8x57 IRS 180gr Naturalis Box of 20", 20),
    ("Barnaul 7.62x39 123gr FMJ 20/25", 20),
    ("Winchester Super-X .30-30 Win 150gr", None),
])
def test_rounds_per_box(title, n):
    assert g.rounds_per_box(title) == n


def test_cost_per_round():
    assert g.cost_per_round(18.99, 50) == 0.3798
    assert g.cost_per_round(0, 50) is None and g.cost_per_round(10, None) is None


def test_parse_title_firearm():
    info = g.parse_title("Glock 19 Gen5 MOS 9mm 4.02in 15+1 Black")
    assert info.kind == "firearm" and info.brand == "Glock"
    assert info.model.model == "Glock 19 Gen 5 MOS"
    assert info.caliber.name == "9×19mm Parabellum"
    assert (info.capacity, info.barrel_length, info.rounds) == (15, 4.02, None)


def test_parse_title_ammo():
    info = g.parse_title("Federal American Eagle 9mm Luger 115gr FMJ, 50/Box", price=18.99)
    assert info.kind == "ammo" and info.model is None
    assert (info.rounds, info.cost_per_round, info.caliber.id) == (50, 0.3798, "9x19mmparabellum")
    json.dumps(info.to_dict())


def test_cli(capsys):
    assert main(["Glock", "19", "Gen", "5", "9mm"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["model"]["model"] == "Glock 19 Gen 5"
