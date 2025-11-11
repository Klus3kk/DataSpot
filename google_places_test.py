import os
import random
import requests
import json
from textwrap import indent

# CONFIGURATION (api is needed here) 
API_KEY = os.getenv("GOOGLE_API_KEY") or "API_KEY"
LOCATION = "52.2297,21.0122"   # Warsaw center (for tests)
RADIUS = 1500                  # in meters
TYPE = "restaurant"            # you can change to: 'park', 'museum' etc etc.
LIMIT = 10                     # max number of places to fetch
MAX_WIDTH = 400                # max width for photos

# Fetch photo urls
def fetch_photo_urls(result, maxwidth = MAX_WIDTH):
    urls = []
    for photo in result.get("photos", []):
        ref = photo.get("photo_reference")
        if not ref:
            continue
        url = (
            "https://maps.googleapis.com/maps/api/place/photo?"
            f"maxwidth={maxwidth}&photoreference={ref}&key={API_KEY}"
        )
        urls.append({
            "url": url,
            "width": photo.get("width"),
            "height": photo.get("height"),
            "attributions": photo.get("html_attributions", []),
        })
    return urls

# Fetch nearby places 
def fetch_nearby_places():
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={LOCATION}&radius={RADIUS}&type={TYPE}&key={API_KEY}"
    )
    resp = requests.get(url, timeout=20).json()
    place_ids = [p.get("place_id") for p in resp.get("results", []) if p.get("place_id")]
    return place_ids[:LIMIT]

# Fetch detailed info about a place
def fetch_place_details(place_id):
    # i gave here all possible fields for demo
    fields = (
        "place_id,name,formatted_address,"
        "geometry,plus_code,"
        "address_components,"
        "types,"
        "opening_hours,photos,reviews,"
        "rating,user_ratings_total,"
        "price_level,business_status,"
        "curbside_pickup,delivery,dine_in,takeout,"
        "serves_beer,serves_breakfast,serves_brunch,serves_dinner,serves_lunch,serves_wine,"
        "wheelchair_accessible_entrance,"
        "website,formatted_phone_number"
    )
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json?"
        f"place_id={place_id}&fields={fields}&key={API_KEY}"
    )
    return requests.get(url, timeout=20).json().get("result", {})

# Print a section of the output
def print_section(title, data):
    print(f"\n=== {title.upper()} ===")
    if not data:
        print("  (no data)")
        return
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"  {k}: {v}")
    elif isinstance(data, list):
        for i, v in enumerate(data, 1):
            if isinstance(v, dict):
                print(f"  {i}.")
                for k2, v2 in v.items():
                    print(indent(f"{k2}: {v2}", "    "))
            else:
                print(f"  {i}. {v}")
    else:
        print(f"  {data}")

def extract_attributes(result):
    keys = [
        "curbside_pickup","delivery","dine_in","takeout",
        "serves_beer","serves_breakfast","serves_brunch",
        "serves_dinner","serves_lunch","serves_wine",
        "wheelchair_accessible_entrance"
    ]
    out = []
    for k in keys:
        if k in result:
            out.append({"attribute_name": k, "value": result.get(k)})
    return out

def extract_address_components(result):
    comps = []
    for c in result.get("address_components", []) or []:
        comps.append({
            "component_type": ",".join(c.get("types", [])),
            "long_name": c.get("long_name"),
            "short_name": c.get("short_name"),
        })
    return comps

def extract_viewport(result):
    vp = (result.get("geometry") or {}).get("viewport") or {}
    ne = vp.get("northeast") or {}
    sw = vp.get("southwest") or {}
    if not ne and not sw:
        return {}
    return {
        "ne_lat": ne.get("lat"),
        "ne_lng": ne.get("lng"),
        "sw_lat": sw.get("lat"),
        "sw_lng": sw.get("lng"),
    }

def extract_geolocation(result):
    loc = (result.get("geometry") or {}).get("location") or {}
    if not loc:
        return {}
    return {"lat": loc.get("lat"), "lng": loc.get("lng")}

# Main program loop
def main():
    print("Fetching nearby places…")
    pool = fetch_nearby_places()
    if not pool:
        print("No results. Try another TYPE/LOCATION/RADIUS.")
        return

    while True:
        pid = random.choice(pool)
        print(f"\nFetching random place: {pid}")
        r = fetch_place_details(pid)
        if not r:
            print("No data returned.")
            continue

        # PLACE
        print_section("PLACE", {
            "place_id": r.get("place_id"),
            "name": r.get("name"),
            "formatted_address": r.get("formatted_address"),
            "business_status": r.get("business_status"),
            "price_level": r.get("price_level"),
        })
        print_section("RATING SUMMARY", {
            "rating": r.get("rating"),
            "user_ratings_total": r.get("user_ratings_total"),
        })

        # GEOLOCATION & VIEWPORT
        print_section("GEOLOCATION", extract_geolocation(r))
        print_section("VIEWPORT", extract_viewport(r))

        # PLUS CODE
        print_section("PLUS CODE", r.get("plus_code", {}))

        # ADDRESS COMPONENTS
        print_section("ADDRESS COMPONENTS", extract_address_components(r))

        # OPENING HOURS
        weekday = (r.get("opening_hours") or {}).get("weekday_text", [])
        print_section("OPENING HOURS", weekday)

        # CONTACT
        print_section("CONTACT", {
            "website": r.get("website"),
            "phone": r.get("formatted_phone_number"),
        })

        # TYPE LABELS
        typelabels = [{"type_name": t} for t in (r.get("types") or [])]
        print_section("TYPE LABELS", typelabels)

        # ATTRIBUTES
        print_section("ATTRIBUTES", extract_attributes(r))

        # PHOTOS
        photos = fetch_photo_urls(r)
        print_section("PHOTOS", photos)

        # REVIEWS
        reviews = r.get("reviews", []) or []
        print_section("REVIEWS", reviews[:3])

        print("\nPress Enter for another random place, or type 'q' to quit.")
        if input("> ").strip().lower().startswith("q"):
            break

if __name__ == "__main__":
    main()
