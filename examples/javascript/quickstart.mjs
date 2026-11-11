// Redfin API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs "Seattle, WA"

const HOST = 'redfin16.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Redfin API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const location = process.argv[2] ?? 'Seattle, WA';

// A small num_homes can return an empty page, so ask for a full one.
const { resolvedLocation, homes } = await get('/search/by-location', {
  location,
  min_beds: 3,
  sort: 'newest',
  num_homes: 50,
});
console.log(`${resolvedLocation.subName}: ${homes.length} homes on this page`);
for (const home of homes.slice(0, 10)) {
  const price = `$${home.price.toLocaleString('en-US')}`;
  console.log(`${price.padStart(12)}  ${home.beds} bd  ${home.address.full}, ${home.address.city}`);
}

if (homes.length) {
  const estimate = await get('/property/estimate', { property_id: homes[0].propertyId });
  // The Redfin Estimate is hidden for some homes.
  const value = estimate.estimate == null || estimate.isHidden
    ? 'not shown'
    : `$${Math.round(estimate.estimate).toLocaleString('en-US')}`;
  console.log(`\nRedfin Estimate for ${homes[0].address.full}: ${value}`);
}
