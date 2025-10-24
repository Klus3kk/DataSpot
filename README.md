# DataSpot

**DataSpot** is a project that allows users to view, search and manage geographic locations on an interactive map integrated with **Google Maps API** or **OpenStreetMap** (we'll decide later on).  
All location data is stored in an **Oracle Database**, with full CRUD operations accessible via a user-friendly interface.

## Features
- Interactive map displaying user-defined locations,
- CRUD operations (Create, Read, Update, Delete) for all records,
- Integration with Google Maps API or OpenStreetMap API for geolocation visualization,
- Search and filtering of locations by name, address, or category,
- Distance calculation between locations using a stored function,
- Secure and validated data input with integrity checks and user-friendly error messages,
- Oracle-stored procedure for adding locations and logging edits,
- Optional user authentication and favorites system.

## Technologies
- **Database:** OracleDB  
- **Frontend:** Oracle APEX   
- **Mapping API:** Google Maps API / OpenStreetMap (Leaflet.js)  
- **Data Modeling:** Oracle SQL Developer Data Modeler  
- **Language:** SQL, PL/SQL

## Database Schema
The database model includes **10 entities** to represent users, locations, categories, and related data:

| Entity | Description |
|---------|-------------|
| `Users` | Stores user information |
| `Locations` | Main table with name, address, coordinates, description |
| `Categories` | Categories of locations |
| `Ratings` | User-submitted ratings |
| `Tags` | Tags for locations |
| `LocationTags` | N:M relation between locations and tags |
| `Photos` | Associated images |
| `EditHistory` | Tracks data modifications |
| `Favorites` | User-saved locations |
| `ErrorReports` | Reported issues with location data |

