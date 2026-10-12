"""Regression test: parse_title on 1,150 real store titles must give the recorded answers.

The same file is used by the JavaScript port (gunsnprices on npm) to keep both implementations identical.
"""
import json
from pathlib import Path

import pytest

from gunsnprices import parse_title

CASES = [json.loads(line) for line in (Path(__file__).parent / "golden.jsonl").read_text(encoding="utf-8").splitlines() if line]


def compact(info):
    d = info.to_dict()
    m = d["model"]
    return {"kind": d["kind"], "brand": d["brand"],
            "model": [m["family"], m["model"], m["generation"], m["configs"], m["features"], m["source"]] if m else None,
            "calibers": [c["id"] for c in d["calibers"]], "capacity": d["capacity"], "barrel_length": d["barrel_length"],
            "rounds": d["rounds"], "cost_per_round": d["cost_per_round"]}


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["args"]["title"][:60])
def test_golden(case):
    assert compact(parse_title(**case["args"])) == case["expected"]
