# Wrap-Up: Phase 1

## Concept Overview
- **Application Goal:** we're building an interactive workspace where users browse and manage location data backed by OracleDB while visualizing points on an external map (we've chosen Google Maps API).

- **Core Capabilities:** search/filter locations, manage categories/tags, capture user-generated metadata (favorites, ratings, notes etc) and expose stored logic (distance calculations, guided inserts) through the UI (which will be Oracle APEX).

## Technology Stack Snapshot
- **Database:** we're using Oracle Database for this. Manual SQL DDL is required (whatever that is lmao), with custom sequences, constraints, one stored function (ex.: `f_calculate_distance`) and one stored procedure (ex.: `p_add_location`).

- **Application Layer:** Oracle APEX for UI, aligned with CRUD flows, report pages, validation, and interactive map integration.

- **Mapping API:** Google Maps API already prototyped; Leaflet/OSM kept as fallback if licensing or quota needs change.

- **Tooling & Docs:** Oracle SQL Developer + Data Modeler for ER design, documentation hidden in (`/docs`).

## Key Decisions & Outcomes
1. **Repository Structure:** locked in the folder layout to cleanly separate database scripts, APEX artifacts, documentation, automation scripts, sample datasets and resources like API keys.

2. **Entity Scope:** targeting at least 10 entities, combining core location data (`Locations`, `Categories`, `Users`, etc.) plus operational/join tables (favorites, tags, API logs) to create relationship diversity (1:1, 1:N, N:M).

3. **Mapping Integration:** proceed with Google Maps first due to existing familiarity; capture API keys/usage constraints early to avoid **surprises** in Phase 4.

4. **Oracle Ecosystem Prep:** need short spikes to validate OracleDB connectivity and APEX workspace access before Phase 3–4; action items logged to avoid blocking later.

5. **Documentation Strategy:** every phase produces artifacts in `/docs` (e.g., ER diagrams, environment notes, test evidence) so that it will be easier to trace progress without digging through code.

## Ready for Phase 2
- ER modeling work begins next: Oracle SQL Developer Data Modeler diagram, ensuring normalization to 3NF and exporting visuals/scripts into `/docs`.
