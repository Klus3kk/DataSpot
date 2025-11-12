# DataSpot

**DataSpot** is a project that allows users to view, search and manage geographic locations
on an interactive map integrated with **Google Maps API** (primary) or **OpenStreetMap** (optional fallback).

All place data is fetched live from the **Google Places API** and processed through an **Oracle Database** backend,
with full CRUD operations accessible via a user-friendly **Oracle APEX** interface.

## Features

* Interactive map displaying dynamically fetched places,
* CRUD operations (Create, Read, Update, Delete) for stored or bookmarked places,
* Integration with **Google Maps API** for live geolocation visualization,
* Search and filtering of results by category, name, or service type,
* Distance calculation between places using a stored PL/SQL function,
* Secure data handling with validation and integrity constraints,
* Stored procedure for inserting and logging user-defined places,
* Optional user features such as session-based favorites or history.

## Technologies

* **Database:** OracleDB
* **Frontend:** Oracle APEX
* **Mapping API:** Google Maps API 
* **Data Modeling:** Oracle SQL Developer Data Modeler
* **Languages:** SQL, PL/SQL, REST API integration (JSON)

## Database Schema

The database model includes **10 entities** to represent real-world geographic and descriptive data:

| Entity             | Description                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `Place`            | Core entity representing a location fetched from the Google Places API. Includes `place_id`, `name`, `address`, `rating`, `price_level`. |
| `GeoLocation`      | Stores latitude and longitude of each place. (1:1 with `Place`)                                                                          |
| `Viewport`         | Defines the visible bounding box around a given location (NE/SW coordinates).                                                            |
| `PlusCode`         | Encodes the location using global and compound geocodes (alternative to traditional address).                                            |
| `AddressComponent` | Individual address elements such as street, city, country, postal code.                                                                  |
| `OpeningHours`     | Weekly opening times in human-readable form.                                                                                             |
| `Photo`            | References to Google-hosted images for the place.                                                                                        |
| `Review`           | User reviews associated with the place, including rating, author, and text.                                                              |
| `TypeLabel`        | Categories and tags assigned by Google (e.g., restaurant, park, museum).                                                                 |
| `Attribute`        | Boolean service and accessibility features (e.g., delivery, takeout, serves_wine, wheelchair_accessible).                                |

See `docs/phase2-data-model.md` for the extended entity catalog, relationship map, and Data Modeler checklist that drive Phase 2 of the project.
