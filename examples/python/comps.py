"""Price one home against its sold comps: Redfin Estimate versus comparable sales.

    python comps.py "<street address with unit, city, state>"

Uses /property/by-address, /property/estimate and /property/similar-sold. The value from
comps is a rough check (median sold price per square foot times the home's size), not an
appraisal.
"""

import sys

from client import get, median, to_date

if len(sys.argv) < 2:
    raise SystemExit('Usage: python comps.py "<full street address, city, state>"')
address = sys.argv[1]


def money(value):
    return f"${value:,.0f}" if value is not None else "-"


match = get("/property/by-address", address=address)
home = match["property"]
print(f"Matched: {match['resolvedAddress']['name']}, {match['resolvedAddress']['subName']}")

# An address without a unit number can match a bare public-record entry for the building,
# with no size or price. The units it also matched are in `alternatives`.
if not home.get("sqft"):
    print("This match has no size on record. Did you mean one of these?")
    for alt in match.get("alternatives") or []:
        print(f"  {alt['name']}, {alt['subName']}")
    raise SystemExit("Re-run with the full address, including the unit.")

print(
    f"{home['propertyType']}, {home['beds']} bd {home['baths']} ba, {home['sqft']} sqft, "
    f"status {home['status'] or 'off market'}, price {money(home['price'])}"
)

estimate = get("/property/estimate", property_id=match["propertyId"])
# The same sale can appear twice in the comps; count each property once.
comps = list(
    {c["propertyId"]: c for c in get("/property/similar-sold", property_id=match["propertyId"])["homes"]}.values()
)

print(f"\n{len(comps)} sold comps")
for comp in comps:
    print(
        f"  sold {to_date(comp['soldDate'])}  {money(comp['price']):>11}  "
        f"{money(comp['pricePerSqft']):>6}/sqft  {comp['sqft'] or '?':>5} sqft  "
        f"{comp['address']['full']}"
    )

per_sqft = median(comp.get("pricePerSqft") for comp in comps)
print()
if per_sqft:
    print(f"Median sold price per sqft: {money(per_sqft)}")
    print(f"Comps value for {home['sqft']} sqft: {money(per_sqft * home['sqft'])}")
if estimate["estimate"] is None or estimate["isHidden"]:
    print("Redfin Estimate: not shown for this home")
else:
    print(f"Redfin Estimate: {money(estimate['estimate'])}")
