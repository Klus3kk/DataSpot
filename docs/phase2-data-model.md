# Phase 2 - Data Modeling Plan

This document captures the design decisions.

## Goals for Phase 2
- Turn the approved concept into a full ER diagram created **in Oracle SQL Developer Data Modeler**.
- Describe every entity, attribute, and relationship so manual SQL DDL can be derived in Phase 3.
- Validate that the design covers at least **10 entities** with mixed relationship types (1:1, 1:N, N:M) and adheres to 3NF.
- Export diagram artifacts (`.dmd` source + `.png/.pdf`) into `/docs/diagrams/` for submission.

## Entity Catalog (exactly what the Google Places script returns)

| Entity | Why it exists | Key Attributes (PK • mandatory FKs) |
| ------ | ------------- | ------------------------------------ |
| `Place` | Core record representing the object returned by the Nearby/Details APIs. | `place_id` (PK, surrogate), `google_place_id` (unique), `name`, `formatted_address`, `business_status`, `price_level`, `rating`, `user_ratings_total`, `website`, `phone`, `created_at`. |
| `GeoLocation` | Captures `geometry.location`. | `place_id` (PK & FK to `Place`), `latitude`, `longitude`, `geohash`, `accuracy_m`. |
| `Viewport` | Stores `geometry.viewport` bounds. | `viewport_id` (PK), `place_id` (FK), `ne_lat`, `ne_lng`, `sw_lat`, `sw_lng`. |
| `PlusCode` | Holds `plus_code.global_code/compound_code`. | `plus_code_id` (PK), `place_id` (FK), `global_code`, `compound_code`. |
| `AddressComponent` | Breaks out the `address_components` array. | `component_id` (PK), `place_id` (FK), `component_type`, `long_name`, `short_name`. |
| `OpeningHoursEntry` | Represents one line of `weekday_text` (and special notes). | `hours_id` (PK), `place_id` (FK), `day_of_week`, `open_time`, `close_time`, `is_overnight`, `note`. |
| `Photo` | Downloadable photo metadata via `photos`. | `photo_id` (PK), `place_id` (FK), `photo_reference`, `photo_url`, `width_px`, `height_px`, `attribution_html`. |
| `Review` | Reviews returned in the details payload. | `review_id` (PK), `place_id` (FK), `author_name`, `author_url`, `rating`, `relative_time_desc`, `text`, `submitted_at`, `language`. |
| `TypeLabel` | Distinct `types` values, deduplicated for reuse. | `type_id` (PK), `type_code`, `description`. |
| `PlaceType` | Junction table mapping each place to all its `types`. | `place_id` (FK), `type_id` (FK), `source` (`google`, `manual`), `confidence_score`; PK = (`place_id`,`type_id`). |
| `PlaceAttribute` | Stores the service/accessibility booleans that the script extracts (delivery, dine_in, wheelchair_accessible_entrance, etc.). | `attribute_id` (PK), `place_id` (FK), `attribute_name`, `value_boolean`, `captured_at`. |

> All 11 entities are straight lifts from `scripts/google_places_test.py`, so the ERD stays grounded in data you already inspected while still exceeding the 10-entity minimum.

## Relationship Summary
- **1:1**: `Place` ↔ `GeoLocation` (shared PK), optional `Place` ↔ `Viewport`, optional `Place` ↔ `PlusCode`.
- **1:N**: `Place` → `AddressComponent`, `OpeningHoursEntry`, `Photo`, `Review`, `PlaceAttribute`.
- **N:M**: `Place` ↔ `TypeLabel` via `PlaceType`, covering the multi-valued `types` array from the API.
- Every FK represents a structure already observed in the script output—no speculative user/account tables needed for Phase 2.

Document each relationship in Data Modeler with appropriate optionality (crow’s foot, mandatory vs optional) to reflect API realities (e.g., some places have no photos or plus codes).

## Normalization & Integrity Notes
- Surrogate PKs everywhere (sequence-driven later) with a unique constraint on `google_place_id`.
- Repeating groups from the API response (`address_components`, `weekday_text`, `photos`, `reviews`) sit in their own tables so the logical model reaches 3NF.
- `TypeLabel` + `PlaceType` normalize the `types` array, and `PlaceAttribute` keeps the boolean feature flags extensible without altering the `Place` table each time Google adds a field.
- Cascade deletes from `Place` into derivative tables (`GeoLocation`, `Viewport`, `PlaceAttribute`, `Photo`, `OpeningHoursEntry`), while `Review` can either cascade or be soft-deleted depending on requirements (capture the decision once the instructor advises).

## Data Modeler Execution Steps
1. **Rough sketch** – copy the entity list above to paper/whiteboard and arrange logical groupings (core place, geometry, classification, service features).
2. **Create new design** – open Oracle SQL Developer Data Modeler → *File → New* → add a logical model named `DataSpot`.
3. **Add entities & attributes** – for each table, input attributes, set PKs/FKs, data types (NUMBER, VARCHAR2, DATE, etc.), and defaults.
4. **Define relationships** – drag connectors between PKs/FKs; set cardinalities (`Mandatory` vs `Optional`).
5. **Annotate** – use comments to note API sources, validation rules, and whether data is read-only vs user-generated.
6. **Validate model** – run *Tools → Validate* to catch missing PKs, orphan FKs, or datatype mismatches.
7. **Export artifacts** – save the `.dmd` design under `/docs/diagrams/DataSpot-phase2.dmd` and export an image/PDF into `/docs/diagrams/`.

## Deliverables Checklist (mirrors TODO Phase 2)
- [ ] Paper/whiteboard ER draft completed (snap a photo for `/docs/diagrams/` optional).
- [ ] Oracle SQL Developer Data Modeler file saved (`/docs/diagrams/DataSpot-phase2.dmd`).
- [ ] Entity definitions finalized (use tables above as baseline, adjust as needed).
- [ ] Relationship coverage confirmed (≥1 of each type, at least 10 active entities).
- [ ] Diagram exported (`.png/.pdf`) and linked from `docs/README.md`.
- [ ] Normalization review done; notes captured in this file (expand the “Normalization” section after review).
