-- Główna encja
create table Place (  
  place_id NUMBER PRIMARY KEY,
  name VARCHAR2(200) NOT NULL,
  formatted_address VARCHAR2(400) NOT NULL,
  business_status VARCHAR2(50),
  price_level NUMBER(1),
  rating NUMBER(2,1),
  user_rating_total NUMBER,
  website VARCHAR2(400),
  phone VARCHAR2(50)
);

-- Relacja: Place 1---< Photo
create table Photo (  
  photo_id NUMBER PRIMARY KEY,
  place_id NUMBER NOT NULL,
  photo_reference VARCHAR2(400) NOT NULL,
  photo_url VARCHAR2(400) NOT NULL,
  width_px NUMBER,
  height_px NUMBER,
  attribution_html VARCHAR2(400),
  constraint fk_photo_place
    foreign key (place_id) references Place(place_id)
);

-- Relacja: Place 1---< Review
create table Review (  
  review_id NUMBER PRIMARY KEY,
  place_id NUMBER NOT NULL,
  author_name VARCHAR2(100) NOT NULL,
  author_url VARCHAR2(400),
  rating NUMBER(2,1),
  relative_time_desc VARCHAR2(100),
  review_text VARCHAR2(2000),
  submitted_at TIMESTAMP,
  language VARCHAR2(20),
  constraint fk_review_place
    foreign key (place_id)  references Place(place_id)
);

-- Relacja: (N:M z Place)
create table TypeLabel (
  type_name VARCHAR2(50) PRIMARY KEY,
  description VARCHAR2(200)
);

-- Tabela Łącząca, relacja: (Place N---< PlaceTypeLabel >---N TypeLabel)
CREATE TABLE PlaceTypeLabel (
  place_id NUMBER NOT NULL,
  type_name VARCHAR2(50) NOT NULL,
  CONSTRAINT pk_place_typelabel
    PRIMARY KEY (place_id, type_name),
  CONSTRAINT fk_pt_place
    foreign key (place_id) REFERENCES Place(place_id),
  CONSTRAINT fk_pt_typelabel
    foreign key (type_name) REFERENCES TypeLabel(type_name)
);

-- Tabela: ATTRIBUTE (atrybuty logiczne miejsca)
-- PK złożony: (place_id, attribute_name)
create table Attribute (
  place_id NUMBER NOT NULL,
  attribute_name VARCHAR2(100) NOT NULL,
  value_boolean NUMBER(1)  DEFAULT 0
    CHECK (value_boolean IN (0,1)),
  CONSTRAINT pk_attribute
    PRIMARY KEY (place_id, attribute_name),
  CONSTRAINT fk_attribute_place
    foreign key (place_id) references Place(place_id)
 );

-- Relacje (Place 1 --0..1 Viewport)
-- Każdy Viewport należy do jednego Place
-- UNIQUE(place_id) realizuje 1:1
create table Viewport (
  viewport_id NUMBER PRIMARY KEY,
  place_id NUMBER NOT NULL UNIQUE,
  ne_lat NUMBER(9,6) NOT NULL,
  ne_lng NUMBER(9,6) NOT NULL,
  sw_lat NUMBER(9,6) NOT NULL,
  sw_lng NUMBER(9,6) NOT NULL,
  CONSTRAINT fk_viewport_place
    foreign key (place_id) references Place(place_id)
);

-- Relacje: (Place 1---< AddressComponent)
create table AddressComponent (
  component_id NUMBER PRIMARY KEY,
  place_id NUMBER NOT NULL,
  component_type VARCHAR2(100) NOT NULL,
  long_name VARCHAR2(200) NOT NULL,
  short_name VARCHAR2(100),
  CONSTRAINT fk_component_place
    foreign key (place_id) references Place(place_id)
 );

-- Relacje: (Place 1---< OpeningHours)
create table OpeningHours (
  hours_id NUMBER PRIMARY KEY,
  place_id NUMBER NOT NULL,
  day_of_week VARCHAR2(20) NOT NULL,
  open_time VARCHAR2(20),
  close_time VARCHAR2(20),
  is_overnight NUMBER(1) CHECK (is_overnight IN (0,1)),
  note VARCHAR2(200),
  CONSTRAINT fk_hours_place
    foreign key (place_id) references Place(place_id)
);

-- Relacje: (Place 1---0..1 PlusCode)
create table PlusCode (
  global_code VARCHAR2(20) PRIMARY KEY,
  place_id NUMBER NOT NULL UNIQUE,
  compound_code VARCHAR2(100),
  CONSTRAINT fk_pluscode_place
    foreign key (place_id) references Place(place_id)
);

-- Relacje: (Place 1---0..1 GeoLocation)
create table GeoLocation (
  geolocation_id NUMBER PRIMARY KEY,
  place_id NUMBER NOT NULL UNIQUE,
  latitude NUMBER(9,6) NOT NULL,
  longitude NUMBER(9,6) NOT NULL,
  CONSTRAINT fk_geolocation_place
    foreign key (place_id) references Place(place_id)
);

-- SEQUENCES
CREATE SEQUENCE seq_place        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_photo        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_review       START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_viewport     START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_component    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_hours        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_geolocation  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- FUNKCJA SKŁADOWANA

-- Wyznaczanie odległości pomiędzy dwo punktami na mapie poprzez wzór Haversine'a
CREATE OR REPLACE FUNCTION distance_between_places(
    p_place_id1 IN NUMBER,
    p_place_id2 IN NUMBER
)
RETURN NUMBER
AS
    lat1   GeoLocation.latitude%TYPE;
    lon1   GeoLocation.longitude%TYPE;
    lat2   GeoLocation.latitude%TYPE;
    lon2   GeoLocation.longitude%TYPE;

    -- promień Ziemi
    R CONSTANT NUMBER := 6371;

    a   NUMBER;
    c   NUMBER;
    d   NUMBER;
BEGIN
    -- pierwsze miejsce
    SELECT latitude, longitude
    INTO lat1, lon1
    FROM GeoLocation
    WHERE place_id = p_place_id1;

    -- drugie miejsce
    SELECT latitude, longitude
    INTO lat2, lon2
    FROM GeoLocation
    WHERE place_id = p_place_id2;

    -- konwersja stopni na radiany
    lat1 := lat1 * (ACOS(-1) / 180);
    lon1 := lon1 * (ACOS(-1) / 180);
    lat2 := lat2 * (ACOS(-1) / 180);
    lon2 := lon2 * (ACOS(-1) / 180);

    -- wzór haversine
    a :=  POWER(SIN((lat2 - lat1) / 2), 2)
          + COS(lat1) * COS(lat2)
          * POWER(SIN((lon2 - lon1) / 2), 2);

    c := 2 * ATAN2(SQRT(a), SQRT(1 - a));

    d := R * c; -- ostateczny dystans [km]

    RETURN d;
END;
/

-- Średni rating miejsca na podstawie zapisywanych recenzji
CREATE OR REPLACE FUNCTION get_place_average_rating(p_place_id IN NUMBER)
RETURN NUMBER
AS
    avg_rating NUMBER;
BEGIN
    SELECT AVG(rating)
    INTO avg_rating
    FROM Review
    WHERE place_id = p_place_id;

    RETURN avg_rating;
END;
/

-- PROCEDURA SKŁADOWANA
  
-- Dodaj recenzję
CREATE OR REPLACE PROCEDURE add_review(
    p_place_id IN NUMBER,
    p_author_name IN VARCHAR2,
    p_rating IN NUMBER,
    p_text IN VARCHAR2,
    p_language IN VARCHAR2
)
AS
BEGIN
    INSERT INTO Review(
        review_id,
        place_id,
        author_name,
        rating,
        text,
        submitted_at,
        language
    )
    VALUES(
        seq_review.NEXTVAL,
        p_place_id,
        p_author_name,
        p_rating,
        p_text,
        SYSTIMESTAMP,
        p_language
    );
END;
/

-- Aktualizacja podstawowych danych miejsca
CREATE OR REPLACE PROCEDURE update_place_basic(
    p_place_id           IN NUMBER,
    p_name               IN VARCHAR2,
    p_formatted_address  IN VARCHAR2,
    p_website            IN VARCHAR2,
    p_phone              IN VARCHAR2
)
AS
BEGIN
    UPDATE Place
    SET 
        name = p_name,
        formatted_address = p_formatted_address,
        website = p_website,
        phone = p_phone
    WHERE place_id = p_place_id;
END;
/

-- Dodawanie nowego miejsca
CREATE OR REPLACE PROCEDURE add_full_place(
    p_name              IN VARCHAR2,
    p_formatted_address IN VARCHAR2,
    p_business_status   IN VARCHAR2,
    p_price_level       IN NUMBER,
    p_lat               IN NUMBER,
    p_lng               IN NUMBER,
    p_ne_lat            IN NUMBER,
    p_ne_lng            IN NUMBER,
    p_sw_lat            IN NUMBER,
    p_sw_lng            IN NUMBER,
    p_website           IN VARCHAR2,
    p_phone             IN VARCHAR2,
    p_new_place_id      OUT NUMBER
)
AS
BEGIN
    p_new_place_id := seq_place.NEXTVAL;

    INSERT INTO Place(
        place_id, name, formatted_address, business_status,
        price_level, website, phone
    ) VALUES (
        p_new_place_id, p_name, p_formatted_address,
        p_business_status, p_price_level, p_website, p_phone
    );

    INSERT INTO GeoLocation(
        geolocation_id, place_id, latitude, longitude
    ) VALUES (
        seq_geolocation.NEXTVAL, p_new_place_id, p_lat, p_lng
    );

    INSERT INTO Viewport(
        viewport_id, place_id,
        ne_lat, ne_lng, sw_lat, sw_lng
    ) VALUES (
        seq_viewport.NEXTVAL, p_new_place_id,
        p_ne_lat, p_ne_lng, p_sw_lat, p_sw_lng
    );
END;
/

