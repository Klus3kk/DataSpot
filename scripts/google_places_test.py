import os
import random
import requests
import json
from textwrap import indent

# CONFIGURATION (api is needed here) 
API_KEY = os.getenv("GOOGLE_API_KEY") or ""
LOCATION = "52.2297,21.0122"   # Warsaw center (for tests)
RADIUS = 1500                  # in meters
TYPE = "restaurant"            # you can change to: 'park', 'museum' etc etc.
LIMIT = 10                     # max number of places to fetch
MAX_WIDTH = 400                # max width for photos

# FETCHING 

def fetch_nearby_places():
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={LOCATION}&radius={RADIUS}&type={TYPE}&key={API_KEY}"
    )
    resp = requests.get(url, timeout=20).json()
    place_ids = [p.get("place_id") for p in resp.get("results", []) if p.get("place_id")]
    return place_ids[:LIMIT]


def fetch_place_details(place_id):
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

# ENTITY BUILDERS

def build_place_entity(r):
    return {
        "place_id": r.get("place_id"),
        "name": r.get("name"),
        "formatted_address": r.get("formatted_address"),
        "business_status": r.get("business_status"),
        "price_level": r.get("price_level"),
        "rating": r.get("rating"),
        "user_ratings_total": r.get("user_ratings_total"),
        "website": r.get("website"),
        "phone": r.get("formatted_phone_number"),
    }


def build_geolocation_entity(r):
    loc = (r.get("geometry") or {}).get("location") or {}
    if not loc:
        return {}
    return {
        "place_id": r.get("place_id"),
        "lat": loc.get("lat"),
        "lng": loc.get("lng"),
    }


def build_viewport_entity(r):
    vp = (r.get("geometry") or {}).get("viewport") or {}
    ne = vp.get("northeast") or {}
    sw = vp.get("southwest") or {}
    if not ne and not sw:
        return {}
    return {
        "place_id": r.get("place_id"),
        "ne_lat": ne.get("lat"),
        "ne_lng": ne.get("lng"),
        "sw_lat": sw.get("lat"),
        "sw_lng": sw.get("lng"),
    }


def build_pluscode_entity(r):
    pc = r.get("plus_code") or {}
    if not pc:
        return {}
    return {
        "place_id": r.get("place_id"),
        "global_code": pc.get("global_code"),
        "compound_code": pc.get("compound_code"),
    }


def build_address_components(r):
    rows = []
    for c in r.get("address_components", []) or []:
        rows.append({
            "place_id": r.get("place_id"),
            "component_type": ",".join(c.get("types", [])),
            "long_name": c.get("long_name"),
            "short_name": c.get("short_name"),
        })
    return rows


def build_opening_hours(r):
    weekday = (r.get("opening_hours") or {}).get("weekday_text", []) or []
    rows = []
    for i, line in enumerate(weekday, start=1):
        rows.append({
            "place_id": r.get("place_id"),
            "line_no": i,
            "text": line,
        })
    return rows


def build_photos(r):
    rows = []
    for photo in r.get("photos", []) or []:
        ref = photo.get("photo_reference")
        if not ref:
            continue
        url = (
            "https://maps.googleapis.com/maps/api/place/photo?"
            f"maxwidth={MAX_WIDTH}&photoreference={ref}&key={API_KEY}"
        )
        rows.append({
            "place_id": r.get("place_id"),
            "photo_reference": ref,
            "photo_url": url,
            "width": photo.get("width"),
            "height": photo.get("height"),
            "attribution_html": "; ".join(photo.get("html_attributions", [])),
        })
    return rows


def build_reviews(r):
    rows = []
    for review in r.get("reviews", []) or []:
        rows.append({
            "place_id": r.get("place_id"),
            "author_name": review.get("author_name"),
            "author_url": review.get("author_url"),
            "rating": review.get("rating"),
            "relative_time_description": review.get("relative_time_description"),
            "text": review.get("text"),
            "language": review.get("language"),
        })
    return rows


def build_typelabels(r):
    rows = []
    for t in (r.get("types") or []):
        rows.append({
            "place_id": r.get("place_id"),
            "type_name": t,
        })
    return rows


def build_attributes(r):
    keys = [
        "curbside_pickup", "delivery", "dine_in", "takeout",
        "serves_beer", "serves_breakfast", "serves_brunch",
        "serves_dinner", "serves_lunch", "serves_wine",
        "wheelchair_accessible_entrance",
    ]
    rows = []
    for k in keys:
        if k in r:
            rows.append({
                "place_id": r.get("place_id"),
                "attribute_name": k,
                "value": r.get(k),
            })
    return rows

# PRINTING 

def print_entity(name, row):
    """Print single-row entity."""
    print(f"\nENTITY: {name}")
    if not row:
        print("  (no data)")
        return
    for k, v in row.items():
        print(f"  {k}: {v}")


def print_entity_list(name, rows):
    """Print multi-row entity (1:N)."""
    print(f"\nENTITY: {name}")
    if not rows:
        print("  (no rows)")
        return
    for i, row in enumerate(rows, start=1):
        print(f"  ROW {i}:")
        for k, v in row.items():
            print(indent(f"{k}: {v}", "    "))
            
# MAIN 

def main():
    print("Fetching nearby places…")
    pool = fetch_nearby_places()
    if not pool:
        print("No results. Try another location.")
        return

    while True:
        pid = random.choice(pool)
        print(f"\n=== RANDOM PLACE FROM API: {pid} ===")
        r = fetch_place_details(pid)
        if not r:
            print("No data returned.")
            continue

        # Build entities
        place = build_place_entity(r)
        geoloc = build_geolocation_entity(r)
        viewport = build_viewport_entity(r)
        pluscode = build_pluscode_entity(r)
        addr_components = build_address_components(r)
        opening = build_opening_hours(r)
        photos = build_photos(r)
        reviews = build_reviews(r)
        types = build_typelabels(r)
        attrs = build_attributes(r)

        # Print entity-style blocks
        print_entity("Place", place)
        print_entity("GeoLocation", geoloc)
        print_entity("Viewport", viewport)
        print_entity("PlusCode", pluscode)
        print_entity_list("AddressComponent", addr_components)
        print_entity_list("OpeningHours", opening)
        print_entity_list("Photo", photos)
        print_entity_list("Review", reviews[:3])  
        print_entity_list("TypeLabel", types)
        print_entity_list("Attribute", attrs)

        print("\nPress Enter for another random place, or type 'q' to quit.")
        if input("> ").strip().lower().startswith("q"):
            break


if __name__ == "__main__":
    main()