# Phase 2 - Data Modeling Plan

This document captures the design decisions.

## Goals for Phase 2
- Turn the approved concept into a full ER diagram created **in Oracle SQL Developer Data Modeler**.
- Describe every entity, attribute, and relationship so manual SQL DDL can be derived in Phase 3.
- Validate that the design covers at least **10 entities** with mixed relationship types (1:1, 1:N, N:M) and adheres to 3NF.
- Export diagram artifacts (`.dmd` source + `.png/.pdf`) into `/docs/diagrams/` for submission.

## Entity Catalog (based on the Google Places script output)

| Entity | Why it exists | Key Attributes / Identifiers |
| ------ | ------------- | ---------------------------- |
| `Place` | Core record representing one location returned by the Places Details API. | Natural identifier `place_id` (from Google); attributes: `name`, `formatted_address`, `business_status`, `price_level`, `rating`, `user_ratings_total`, `website`, `phone`. |
| `GeoLocation` | Captures `geometry.location` (latitude/longitude) for the place. | Identified by `place_id` (1:1 with `Place`); attributes: `latitude`, `longitude`. |
| `Viewport` | Stores `geometry.viewport` bounds used by the map to zoom correctly. | Identifier `viewport_id` (surrogate) or identifying relationship to `GeoLocation`; attributes: `ne_lat`, `ne_lng`, `sw_lat`, `sw_lng`. |
| `PlusCode` | Holds `plus_code.global_code` / `compound_code` if provided. | Identifier `global_code` (natural); attributes: `compound_code`. |
| `AddressComponent` | Breaks out the `address_components[]` array (street number, route, city, country, postal code, etc.). | Identifier `component_id`; attributes: `component_type`, `long_name`, `short_name`. Each row is linked to one `Place`. |
| `OpeningHours` | Represents a single line of the `opening_hours.weekday_text[]` list (e.g. “Monday: 1:00–22:00”). | Identifier `hours_id`; attributes such as `day_of_week`, `open_time`, `close_time`, `is_overnight`, `note`. Multiple rows per `Place`. |
| `Photo` | Downloadable photo metadata coming from the `photos[]` array. | Identifier `photo_id`; attributes: `photo_reference`, `photo_url`, `width_px`, `height_px`, `attribution_html`. Multiple rows per `Place`. |
| `Review` | Reviews returned in the details payload (`reviews[]`). | Identifier `review_id`; attributes: `author_name`, `author_url`, `rating`, `relative_time_desc`, `text`, `submitted_at`, `language`. Multiple rows per `Place`. |
| `TypeLabel` | Distinct classification labels from the `types[]` array (e.g. `restaurant`, `food`, `point_of_interest`). | Identifier `type_name` (natural). Linked to many places via an N:M relationship. |
| `Attribute` | Service/accessibility flags extracted by the script (e.g. `delivery`, `dine_in`, `takeout`, `serves_wine`, `wheelchair_accessible_entrance`). | Composite identifier (`place_id`, `attribute_name`); attributes: `value_boolean`. One row per flag per `Place`. |

> These 10 entities are directly grounded in the JSON structure printed by `scripts/google_places_test.py` (sections: PLACE, GEOLOCATION, VIEWPORT, PLUS CODE, ADDRESS COMPONENTS, OPENING HOURS, TYPE LABELS, ATTRIBUTES, PHOTOS, REVIEWS).

## Relationship Summary

- **1:1**
  - `Place` ↔ `GeoLocation` (each place has exactly one coordinate pair).
  - `GeoLocation` ↔ `Viewport` (one viewport rectangle per coordinate set).
  - Optional `Place` ↔ `PlusCode` (only where Google returns a plus code).

- **1:N**
  - `Place` → `AddressComponent` (one place, many components of the address).
  - `Place` → `OpeningHours` (one place, multiple weekday entries).
  - `Place` → `Photo` (one place, multiple photos).
  - `Place` → `Review` (one place, multiple reviews).
  - `Place` → `Attribute` (one place, multiple boolean flags).

- **N:M**
  - `Place` ↔ `TypeLabel` — a place can have many labels (restaurant, food, etc.), and one label can apply to many places.  
    At the relational level this will become an intersection table (e.g. `PLACE_TYPE`), but at the ER level it is modeled as a direct M:N relationship.

Optionality should follow the API reality: some places may not have photos, reviews, plus codes or opening hours, but every dependent entity must be linked to exactly one `Place`.

## Normalization & Integrity Notes

- Each entity has a clear identifier (natural or surrogate).  
- Repeating groups from the API (`address_components`, `weekday_text`, `photos`, `reviews`, `types`, boolean flags) are moved into separate entities so the logical model satisfies 3NF.
- The M:N relationship `Place`–`TypeLabel` will be transformed into a junction table during relational design, enforcing uniqueness (`place_id`, `type_name`).
- `Attribute` keeps service/accessibility features extensible: new attributes from Google can be stored as new rows instead of altering the `Place` structure.
- In the relational model, deletes on `Place` should cascade into dependent tables (`GeoLocation`, `Viewport`, `PlusCode`, `AddressComponent`, `OpeningHours`, `Photo`, `Review`, `Attribute`); the exact policy for `Review` can be finalized after instructor feedback.

## Data Modeler Execution Steps

1. **Rough sketch** – copy the entity list above to paper/whiteboard and arrange logical groupings (core place, geometry, address, classification, reviews/media, attributes).
2. **Create new design** – open Oracle SQL Developer Data Modeler → *File → New* → add a logical model named `DataSpot`.
3. **Add entities & attributes** – for each entity, input attributes, set identifiers (Primary UID), and choose data types (NUMBER, VARCHAR2, DATE, etc.).
4. **Define relationships** – connect entities with relationships and set cardinalities (1:1, 1:N, N:M) and optionality.
5. **Annotate** – use comments to note which part of the Google Places JSON each entity/attribute comes from.
6. **Validate model** – run *Tools → Validate* to catch missing identifiers or inconsistent relationships.
7. **Export artifacts** – save the `.dmd` design under `/docs/diagrams/DataSpot-phase2.dmd` and export an image/PDF into `/docs/diagrams/`.

## Deliverables Checklist (mirrors TODO Phase 2)

- [ ] Paper/whiteboard ER draft completed (optional photo in `/docs/diagrams/`).
- [ ] Oracle SQL Developer Data Modeler file saved (`/docs/diagrams/DataSpot-phase2.dmd`).
- [ ] Entity definitions finalized (using the catalog above).
- [ ] Relationship coverage confirmed (at least one 1:1, 1:N and N:M).
- [ ] Diagram exported (`.png/.pdf`) and linked from `docs/README.md`.
- [ ] Normalization review done; notes captured in this file (expand the “Normalization” section after review).
