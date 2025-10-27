# TODO 
## 1. CORE OBJECTIVE
Design, implement, and document an interactive application for browsing and managing location data using OracleDB as the backend and an external mapping API for visualization.

## 2. TASK CHECKLIST

### Phase 1 — Planning and Setup
- [x] Define overall project concept and goals  
- [x] Confirm project fits course requirements (10 entities, function, procedure, CRUD)  
- [x] Write short application description for approval  
- [ ] Create repository structure (`/sql`, `/apex`, `/docs` etc. or something similar)  
- [x] Add initial `README.md` and `TODO.md` to version control
- [ ] Experiment with technologies given.

**Target:** October 27, 2025  

### Phase 2 — Data Modeling
- [ ] Draft initial Entity–Relationship (ER) model on paper or draw.io  
- [ ] Create full ER diagram in **Oracle SQL Developer Data Modeler**
- [ ] Define entity names, attributes, and primary/foreign keys  
- [ ] Verify minimum 10 entities and variety of relationships (1:1, 1:N, N:M)  
- [ ] Export diagram for documentation  
- [ ] Review and refine logical model with normalization up to 3NF  

**Target:** November 5, 2025  

### Phase 3 — Relational Schema and SQL DDL
- [ ] Transform ER diagram into manual SQL DDL scripts (no auto-generation)  
- [ ] Implement tables, constraints, foreign keys, and cascading rules  
- [ ] Create necessary **sequences** for ID generation  
- [ ] Write one **stored function** (`f_calculate_distance`)  
- [ ] Write one **stored procedure** (`p_add_location`)  
- [ ] Add optional **indexes** for text search and performance  
- [ ] Test all scripts in Oracle SQL Developer  

**Target:** November 8, 2025  

### Phase 4 — Application Development
- [ ] Set up **Oracle APEX** environment  
- [ ] Connect APEX workspace with OracleDB schema  
- [ ] Build main map page integrating **Google Maps API** or **Leaflet.js (OSM)**  
- [ ] Implement CRUD pages for all major entities (`Locations`, `Categories`, `Users`, etc.)  
- [ ] Create search and filter functionality  
- [ ] Add validation and user-friendly error handling (no raw error messages, they must be custom)   
- [ ] Connect stored procedure and function to interface (interactive usage)  
- [ ] Add “report” or “read-only” page for summarized data  

**Target:** November 11, 2025  

### Phase 5 — Testing and Finalization
- [ ] Perform functional testing (insert/update/delete/search)  
- [ ] Validate integrity constraints and sequence generation  
- [ ] Verify output of stored function and procedure  
- [ ] Test API calls (map loading, coordinate retrieval, marker placement) [especially where it comes to API limit for data extracting]  
- [ ] Prepare screenshots and short demo documentation  
- [ ] Submit final version of scripts, diagrams, and APEX app  

**Target:** November 12, 2025  
