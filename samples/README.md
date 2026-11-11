# Sample responses

Example `200` responses for eight Redfin API endpoints, copied from the API's public
documentation. Long arrays are cut to their first three items, and agent fields are removed.
Field names and values are otherwise unchanged. File names follow the endpoint path.

Privacy review (4 Nov 2026): the homes keep street, city and ZIP but not their house or unit number (`address.full` and `resolvedAddress.name` show the street only, `unit` reads `[removed]`), their `url` reads `[removed]`, and their coordinates are rounded to three decimals (about 100 m). The apartment community in `autocomplete.json` is unchanged.

| File | Request |
|---|---|
| `autocomplete.json` | `GET /autocomplete?q=Seattle` |
| `search_by-location.json` | `GET /search/by-location?location=Seattle, WA` |
| `search_price-reduced.json` | `GET /search/price-reduced?region_id=30818&region_type=city` |
| `property_by-address.json` | `GET /property/by-address?address=...` (a Seattle townhouse address) |
| `property_estimate.json` | `GET /property/estimate?property_id=30972007` |
| `property_similar-sold.json` | `GET /property/similar-sold?property_id=109905251` |
| `property_history.json` | `GET /property/history?property_id=173648946` |
| `market_trends.json` | `GET /market/trends?region_id=16163&region_type=city` |

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
