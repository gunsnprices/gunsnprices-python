"""Command line: ``python -m gunsnprices "Glock 19 Gen 5 9mm 15rd"`` prints the parsed title as JSON.

Without arguments, titles are read from standard input, one per line (JSON Lines out).
"""
import argparse
import json
import sys

from . import __version__, parse_title


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gunsnprices", description="Parse firearm and ammunition product titles.")
    ap.add_argument("title", nargs="*", help="product title (reads stdin when omitted)")
    ap.add_argument("--brand", help="manufacturer, if known")
    ap.add_argument("--price", type=float, help="listing price (gives cost per round for ammo)")
    ap.add_argument("--kind", choices=["firearm", "ammo"], help="skip the firearm/ammo guess")
    ap.add_argument("--version", action="version", version=f"gunsnprices {__version__}")
    a = ap.parse_args(argv)
    titles = [" ".join(a.title)] if a.title else (line.strip() for line in sys.stdin)
    for t in titles:
        if t:
            info = parse_title(t, brand=a.brand, price=a.price, kind=a.kind)
            print(json.dumps(info.to_dict(), ensure_ascii=False, indent=None if not a.title else 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
