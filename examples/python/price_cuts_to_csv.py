"""Export recent price cuts in a place to CSV, with the original list price of each home.

    python price_cuts_to_csv.py "Austin, TX" --limit 10

Searches homes whose price was cut in the last 30 days, then reads each home's history to
find the price it was first listed at. That is one extra call per home, so --limit caps it.
"""

import argparse
import csv

from client import current_listing_events, get, to_date

parser = argparse.ArgumentParser()
parser.add_argument("location", nargs="?", default="Austin, TX")
parser.add_argument("--limit", type=int, default=10, help="homes to look up (1 call each)")
parser.add_argument("--out", default="price_cuts.csv")
args = parser.parse_args()

results = get(
    "/search/by-location",
    location=args.location,
    price_reduced="within-30-days",
    num_homes=100,
)
homes = results["homes"][: args.limit]
print(f"{results['resolvedLocation']['subName']}: {len(results['homes'])} reduced homes on this page")

rows = []
for home in homes:
    history = get("/property/history", property_id=home["propertyId"])
    events = current_listing_events(history, home.get("listedDate"))
    # The first "Listed" (or "Coming Soon") event of the current listing holds the original
    # asking price. When the history has not caught up with the listing, leave it blank
    # rather than guess.
    starts = [e for e in events if e["price"] and e["event"] in ("Listed", "Relisted", "Coming Soon")]
    original = starts[-1]["price"] if starts else None
    cut = original - home["price"] if original else None
    rows.append(
        {
            "address": home["address"]["full"],
            "city": home["address"]["city"],
            "zip": home["address"]["zip"],
            "property_type": home["propertyType"],
            "beds": home["beds"],
            "sqft": home["sqft"],
            "listed_on": to_date(home.get("listedDate")),
            "original_price": original,
            "current_price": home["price"],
            "cut": cut,
            "cut_pct": round(100 * cut / original, 1) if cut else None,
            "price_changes": sum(e["event"] == "Price Changed" for e in events),
            "url": home["url"],
        }
    )
    was = f"${original:,}" if original else "not in history"
    print(f"  {home['address']['full']}: {was} -> ${home['price']:,}")

with open(args.out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["address"])
    writer.writeheader()
    writer.writerows(rows)
print(f"\nWrote {len(rows)} rows to {args.out}")
