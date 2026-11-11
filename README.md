# Redfin API and Scraper

The Redfin API returns US real estate data from redfin.com as JSON: homes for sale, rentals
and recently sold homes, with full property details, photos, price and tax history, public
records, the Redfin Estimate home value and its history, rent estimates, sold comps, agents
and housing market trends. Redfin has no public API for its listings, so this REST API is
the way to get them into your own code without running and maintaining a Redfin scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/redfin-api?utm_source=github&utm_medium=readme&utm_campaign=redfin-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/redfin16
- Product page: https://happyendpoint.com/library/redfin-api?utm_source=github&utm_medium=readme&utm_campaign=redfin-api
- Postman documentation: https://documenter.getpostman.com/view/56555678/2sBYHVwKWh
- Postman collection (fork and run): https://www.postman.com/happyendpoints-team/redfin-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://redfin16.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 66, all `GET` |
| Coverage | United States, in Redfin's markets: cities, ZIP codes, neighborhoods, counties, school districts |
| Listing types | For sale, coming soon, pending, recently sold, rentals, new construction, foreclosures |
| Page size | Up to 500 homes per page (`num_homes`, default 350) |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Search**
- Homes for sale, rentals and recently sold homes by free-text place (`Seattle, WA`, `98109`), region id, point and radius, map polygon, a pasted Redfin page URL, or a list of known ids
- Up to 48 search parameters: price, beds, baths, size, lot, year built, HOA, property tax, monthly payment, days on market, price cuts, open houses, walk, transit and school scores, and more
- Ready-made searches for new listings, price-reduced homes, open houses, new construction, foreclosures, fixer-uppers and waterfront homes

**Homes**
- Home cards by property id, listing id, street address or Redfin URL
- Listing summary, every photo with room tags, 3D tours, amenities, schools and the listing agent
- Sale and tax history, county public records and the land parcel

**Values and comps**
- The Redfin Estimate, with about five years of monthly history next to city, county and ZIP trends
- Estimated monthly rent with its low to high band
- Similar homes for sale and sold comps, price-cut details, mortgage inputs and today's rates

**Market and area**
- Monthly housing market trends for a city, ZIP, neighborhood, county or state, and nationally
- Redfin's Compete Score, climate risk, Walk Score, schools with GreatSchools ratings, map clusters

**Agents**
- Agent search by area, profiles, deal statistics, past deals and client reviews

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/redfin16). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

`/search/by-location` takes a place in plain text, so no lookup is needed first:

```bash
curl "https://redfin16.p.rapidapi.com/search/by-location?location=Seattle%2C%20WA&min_beds=3&num_homes=50" \
  -H "x-rapidapi-host: redfin16.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py "Seattle, WA"
```

```python
from client import get

results = get("/search/by-location", location="Seattle, WA", min_beds=3, num_homes=50)
for home in results["homes"]:
    print(home["price"], home["beds"], home["address"]["full"], home["propertyId"])

estimate = get("/property/estimate", property_id=results["homes"][0]["propertyId"])
print(estimate["estimate"])  # None when Redfin hides it
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs "Seattle, WA"
```

---

## Example response

`GET /search/by-location?location=Seattle, WA`, trimmed to one home. Values are the example
in the API's public documentation. More responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "resolvedLocation": {
      "name": "Seattle",
      "subName": "Seattle, WA, USA",
      "regionId": 16163,
      "regionType": "city"
    },
    "homes": [
      {
        "propertyId": "12318639",
        "listingId": "224399525",
        "propertyType": "townhouse",
        "status": "active",
        "price": 950000,
        "priceType": "list",
        "beds": 3,
        "baths": 2.25,
        "sqft": 1670,
        "lastSoldDate": "2016-09-13T07:00:00Z",
        "address": {
          "full": "Franklin Ave E",
          "city": "Seattle",
          "state": "WA",
          "zip": "98102",
          "latitude": 47.649,
          "longitude": -122.321
        },
        "photoCount": 26
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://redfin16.p.rapidapi.com`

### Search

| Endpoint | Returns |
|---|---|
| `GET /autocomplete` | Location typeahead: matching cities, ZIP codes, neighborhoods, counties, schools and school districts |
| `GET /search` | Homes for sale in a region or polygon |
| `GET /search/by-region` | Homes for sale in a region: the region-id form of /search (identical inputs and results) |
| `GET /search/by-location` | Homes for sale in a place named in free text, in one call: no region id needed |
| `GET /search/by-coordinates` | Homes for sale within radius_miles of a point: "what is for sale near here" |
| `GET /search/by-polygon` | Homes for sale inside a map polygon: a drawn area, a school zone, a neighborhood outline |
| `GET /search-by-url` | Homes for sale for a Redfin region page URL |
| `GET /search/by-url` | Homes for sale for a Redfin region page URL: same as /search-by-url |
| `GET /search/by-ids` | Home cards for known ids in one call: refresh a saved list or a watch list |
| `GET /rentals` | Rentals in a region or polygon |
| `GET /rentals/by-region` | Rentals in a region: the region-id form of /rentals (identical inputs and results) |
| `GET /rentals/by-location` | Rentals in a place named in free text, in one call: no region id needed |
| `GET /rentals/by-coordinates` | Rentals within radius_miles of a point: "apartments near this office" |
| `GET /sold` | Recently sold homes in a region or polygon |
| `GET /sold/by-region` | Recently sold homes in a region: the region-id form of /sold (identical inputs and results) |
| `GET /sold/by-location` | Recently sold homes in a place named in free text, in one call |
| `GET /sold/by-polygon` | Recently sold homes inside a map polygon: comparable sales around a subject home or across a drawn area |
| `GET /search/new-listings` | Homes for sale that came on the market recently: at most listed_within_days days ago (default 7) |
| `GET /search/price-reduced` | Homes for sale whose price was cut, by when the cut happened |
| `GET /search/open-houses` | Homes for sale with an upcoming open house, with the open-house times on each card |
| `GET /search/new-construction` | New-construction homes for sale: builder listings and plans |
| `GET /search/foreclosures` | Foreclosures for sale: agent-listed foreclosures and bank-owned homes |
| `GET /search/fixer-uppers` | Fixer-upper homes for sale (homes listed as needing work) |
| `GET /search/waterfront` | Waterfront homes for sale |

### Home lookup

| Endpoint | Returns |
|---|---|
| `GET /property` | One home card by property id or listing id |
| `GET /property-by-url` | The same home card as /property, looked up from a Redfin home page URL |
| `GET /property/by-address` | Look up a home by its street address |

### Home details

| Endpoint | Returns |
|---|---|
| `GET /property/summary` | The listing summary of a home: status, dates, address, agents, remarks, highlighted facts and flags |
| `GET /property/photos` | Every photo of a home in five sizes (thumbnail to full), with room tags, 3D walkthrough tours and listing videos |
| `GET /property/details` | Assigned and nearby schools with ratings, the school districts serving a home, and the MLS listing agent and broker with phone numbers |
| `GET /property/amenities` | Every amenity and feature recorded for a home, grouped by section (for example Parking, Interior, Exterior, Financial) |
| `GET /property/estimate` | The Redfin Estimate of a home's market value: one value in US dollars, with no low/high range |
| `GET /property/estimate-history` | Monthly Redfin Estimate history of a home (about five years, oldest first), next to the city, county and ZIP market trends over the same months |
| `GET /property/mortgage` | Mortgage calculator inputs for a home |
| `GET /property/rental-estimate` | Redfin's estimated monthly rent for a home in US dollars, with its low to high band |
| `GET /property/walk-score` | Walk Score, Bike Score and Transit Score (0 to 100) for a home's location |
| `GET /property/price-drop` | Whether a listing's asking price was recently cut and, when it was, by how much |
| `GET /property/market-heat` | How competitive the market around a home is |
| `GET /property/climate-risk` | Climate risk for one home or a point on a home's parcel |
| `GET /property/similar-homes` | Homes for sale that are similar to a given home and nearby, as compact cards |
| `GET /property/similar-sold` | Sold homes comparable to a given home (comps), as compact cards |
| `GET /property/popularity` | How much attention a listing is getting |
| `GET /property/tour-insights` | Redfin agents' tour notes for a home |
| `GET /property/tour-availability` | When a listing can be toured in person |
| `GET /property/parcel` | The land parcel under a home |
| `GET /property/agent` | The listing agents and buyer's agents on a home's listing, with the full agent block |
| `GET /property/redfin-agent` | The Redfin agent Redfin assigns to a home's area: not the listing agent |
| `GET /property/history` | A home's sale and tax history |
| `GET /property/public-records` | County public-record facts for a home |

### Agents

| Endpoint | Returns |
|---|---|
| `GET /agents/autocomplete` | Start here to find real estate agents: a typeahead for places and agent names |
| `GET /agents/search` | Every Redfin and partner agent serving a city, neighborhood, county or ZIP code |
| `GET /agents/detail` | An agent's public profile |
| `GET /agents/stats` | An agent's deal statistics |
| `GET /agents/deals` | An agent's deals, as home cards |
| `GET /agents/reviews` | Every client review of an agent, page by page |

### Market and region data

| Endpoint | Returns |
|---|---|
| `GET /region` | Identity and boundary of a Redfin region: a city, ZIP code, neighborhood, county, state, school or school district |
| `GET /geo/zip-info` | Look up a 5-digit US ZIP code and get its Redfin region |
| `GET /market-stats` | Market snapshot for an area: size a search before paging through it |
| `GET /market/trends` | Monthly housing-market trends for a city, ZIP, neighborhood, county or state |
| `GET /market/trends/national` | United States housing-market trends, with Redfin's explanation of each metric |
| `GET /market/hotness` | How competitive a region's housing market is: Redfin's Compete Score (0 to 100) with its components |
| `GET /market/climate-risk` | Climate risk for a whole city, ZIP, neighborhood or county |
| `GET /schools` | Schools with GreatSchools ratings, enrollment, district and location |
| `GET /map-clusters` | Map clusters for an area, for drawing a pin or heat map |
| `GET /mortgage/rates` | Today's advertised mortgage rates on Redfin for purchase and refinance |
| `GET /status` | Service health |

---

## Things to know about the data

These come from running the examples against the live API on 28 October 2026. They are
the mistakes that produce wrong numbers rather than errors.

- **A small `num_homes` can return an empty page.** A search with `num_homes=5` came back
  with no homes for Austin, while `num_homes=40` returned 29. Ask for a full page (50 or
  more) and stop when a page comes back short.
- **`numHomes` counts the homes on this page,** not every home in the area. Keep
  `num_homes` the same while paging with `page`.
- **The Redfin Estimate can be hidden.** For some homes `/property/estimate` returns
  `estimate: null` with `isHidden: true`. Check before you use it; every example here does.
- **Price history is not only this listing.** `/property/history` holds every listing the
  home ever had, including rentals ("Listed for Rent" at $2,395 next to a $350,000 sale
  listing), and can list one event twice, once per source (the MLS and Zillow, or MLS and
  public records). `client.current_listing_events()` keeps only events since the card's
  `listedDate`, without duplicates.
- **History can lag the listing.** For three of five recently reduced Austin homes, the
  history did not yet include the current listing. `price_cuts_to_csv.py` leaves the
  original price blank in that case instead of guessing.
- **Public-record sales can have no price.** In the Texas homes we tested, "Sold (Public
  Records)" events had `price: null`. Sold comps from `/property/similar-sold` still carry
  the MLS sale price.
- **Dates come in three formats:** ISO strings on search cards (`listedDate`,
  `lastSoldDate`), Unix seconds on sold comps (`soldDate`), and Unix milliseconds in price
  history and estimates. `client.to_date()` handles all three.
- **Sold comps can repeat a home.** One `/property/similar-sold` response listed the same
  property twice. De-duplicate on `propertyId` before you take a median; `comps.py` does.
- **An address without its unit can match the building.** A Seattle townhouse address
  without its unit matched a public-record entry with no price, beds or size, and the units came back in
  `alternatives`. Include the unit number.
- **Region types are words on searches, numbers on `/autocomplete`.** Autocomplete rows
  carry `regionType: 6` for a city, while the search endpoints take `region_type=city`.
  `/search/by-location` returns the word form in `resolvedLocation`, so reuse that.
- **`propertyTypeRaw` and `statusRaw` change type.** They are numbers on search cards and
  words on `/property/by-address` (`"TOWNHOUSE"`). Use `propertyType` and `status`, which
  are the same everywhere.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Free-text search, the newest listing's Redfin Estimate and its price history |
| [`examples/python/comps.py`](examples/python/comps.py) | One home by address: Redfin Estimate against the median price per square foot of its sold comps |
| [`examples/python/price_cuts_to_csv.py`](examples/python/price_cuts_to_csv.py) | Homes reduced in the last 30 days, with original and current price and the size of the cut, to CSV |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Documented example responses for eight endpoints |

---

## API or your own Redfin scraper

A homemade Redfin scraper works until the page structure, the anti-bot rules or the
internal endpoints change, and then it returns nothing or the wrong fields. This API returns
the same homes as documented JSON with a stable contract, so the work you keep is the
analysis, not the parser. If you need a one-off national file or a recurring export rather
than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=redfin-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Redfin homes
without code:

```json
{
  "mcpServers": {
    "redfin": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: redfin16.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Redfin API?

Redfin does not publish a public developer API for its listings. It does publish free
downloadable housing market data in its [Data Center](https://www.redfin.com/news/data-center/).
For listings, homes and values, this API, built and maintained by Happy Endpoint and
independent of Redfin, provides access as REST and JSON.

### Is there a free Redfin API?

Plans, including what each one allows, are on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/redfin16), where every endpoint can
also be tested in the browser.

### How do I use the Redfin API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI headers.
[`examples/python/client.py`](examples/python/client.py) is a short client with helpers for
Redfin's date formats and price history, and the other scripts in that folder are ready to run.

### Can I get the Redfin Estimate through the API?

Yes. `/property/estimate` returns the current Redfin Estimate, `/property/estimate-history`
about five years of monthly values, and `/property/rental-estimate` the estimated monthly
rent. The estimate is not shown for every home, so check for `null`.

### Can I get sold prices and comps from Redfin?

Yes. `/sold/by-location` and the other sold searches return recently sold homes with their
sale price, and `/property/similar-sold` returns the sold comps Redfin shows for one home.
[`comps.py`](examples/python/comps.py) turns them into a quick value check.

### Is this an alternative to the Zillow API?

For many uses, yes. Zillow no longer offers a general public API for listings and Zestimates.
This API covers the same kinds of data from Redfin: homes for sale, sold homes, rentals, a
home value estimate with history, and price history.

### Where is the Redfin API documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the endpoint
tables above summarise them. Example responses are in [`samples/`](samples/).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [rent-com-api](https://github.com/happyendpointhq/rent-com-api) - US rental listings, with a watchlist and CSV export
- [yad2-api](https://github.com/happyendpointhq/yad2-api) - Israel listings with registered sale prices, and the same kind of comparables example
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - asking versus paid prices in Dubai
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: hello@happyendpoint.com

## Licence

MIT. See [LICENSE](LICENSE).
