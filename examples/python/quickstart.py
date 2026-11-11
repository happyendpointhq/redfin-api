"""Search a place for homes for sale, then open the newest listing.

    python quickstart.py "Seattle, WA"
"""

import sys

from client import current_listing_events, get, to_date

location = sys.argv[1] if len(sys.argv) > 1 else "Seattle, WA"

# 1. Free-text search: no region id needed. Ask for a full page; a small num_homes can
#    come back empty even when the area has plenty of homes.
results = get(
    "/search/by-location",
    location=location,
    min_beds=3,
    sort="newest",
    num_homes=50,
)
place = results["resolvedLocation"]
homes = results["homes"]
print(f"{place['subName']} (region {place['regionId']}, {place['regionType']})")
print(f"{len(homes)} homes on this page\n")
for home in homes[:10]:
    address = home["address"]
    print(
        f"${home['price']:>11,}  {home['beds']} bd {home['baths']} ba "
        f"{home['sqft'] or '?':>5} sqft  {address['full']}, {address['city']}  "
        f"listed {to_date(home.get('listedDate'))}"
    )

if not homes:
    raise SystemExit("No homes on this page. Try fewer filters or another place.")

# 2. The Redfin Estimate for the first home. It can be hidden for some homes, so check
#    before using it.
home = homes[0]
estimate = get("/property/estimate", property_id=home["propertyId"])
print(f"\n{home['address']['full']}: list price ${home['price']:,}")
if estimate["estimate"] is None or estimate["isHidden"]:
    print("Redfin Estimate: not shown for this home")
else:
    print(f"Redfin Estimate: ${estimate['estimate']:,.0f}")

# 3. What happened to this listing so far. The full history also holds old sales, rental
#    listings and duplicate events, so keep only the current listing's events.
history = get("/property/history", property_id=home["propertyId"])
events = current_listing_events(history, home.get("listedDate"))
if not events:
    print("  (the price history has not recorded this listing yet)")
for event in events:
    price = f"${event['price']:,}" if event["price"] else "-"
    print(f"  {to_date(event['date'])}  {event['event']:<16} {price}")
