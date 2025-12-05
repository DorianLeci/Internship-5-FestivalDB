CREATE TABLE country(
	country_id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL
);

CREATE TABLE city(
	city_id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	postal_code VARCHAR(10),
	country_id INT NOT NULL REFERENCES country(country_id)
	
		
);

CREATE TABLE visitor(
	visitor_id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	surname VARCHAR(30) NOT NULL,
	email VARCHAR(50),
	birth_date DATE,
	city_id INT NOT NULL REFERENCES city(city_id)
);


CREATE TYPE festival_status AS ENUM('Planiran','Aktivan','Zavrsen');

CREATE TABLE festival(
	festival_id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	capacity INT NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	has_visitor_camp BOOL,
	status festival_status NOT NULL,
	city_id INT NOT NULL REFERENCES city(city_id)	
);

CREATE TABLE band(
	band_id SERIAL PRIMARY KEY,
	band_name VARCHAR(40) NOT NULL,
	num_of_members INT 
);


CREATE TYPE music_genre AS ENUM(
    'Rock',
    'Pop',
    'Jazz',
    'House',
    'HipHop',
    'Classical',
    'Blues',
    'Country',
    'Metal',
    'Soul',
    'Reggae',
    'Funk',
    'Techno',
    'Disco',
    'R&B',
    'Alternative',
    'Indie',
    'Punk',
    'Electronic',
    'Trance',
    'Dubstep',
    'Folk',
    'Gospel',
    'Ska',
    'Grunge',
    'Ambient',
    'Opera',
    'Latin',
    'K-Pop',
    'J-Pop',
    'EDM',
    'Hardstyle',
    'Drum & Bass',
    'Chillout',
    'Lounge');

CREATE TYPE performer_type AS ENUM('Solo','DJ','Band_Member');

CREATE TABLE performer(
	performer_id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	genre music_genre,
	is_active BOOL,
	type performer_type NOT NULL,
	country_id INT NOT NULL REFERENCES country(country_id),
	band_id INT REFERENCES band(band_id)
);



CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE festival_performer(
	festival_performer_id SERIAL PRIMARY KEY,
	performer_id INT NOT NULL REFERENCES performer(performer_id) ON DELETE CASCADE,
	festival_id INT NOT NULL REFERENCES festival(festival_id) ON DELETE CASCADE,
	festival_period DATERANGE,
	
	UNIQUE(performer_id,festival_id)
);


ALTER TABLE festival_performer
ADD CONSTRAINT no_overlaping_festivals_for_performer
	EXCLUDE USING gist(
		performer_id WITH =,
		festival_period WITH &&
	);

CREATE TYPE festival_location AS ENUM (
	'Main',
    'Forest',
    'Beach',
    'Park',
    'Stadium',
    'Warehouse',
    'Rooftop',
    'Garden',
    'Riverbank',
    'Desert');


CREATE TABLE stage(
	stage_id SERIAL PRIMARY KEY,
	name VARCHAR(20),
	capacity INT,
	is_covered BOOL,
	location festival_location,
	festival_id INT NOT NULL REFERENCES festival(festival_id) ON DELETE CASCADE
	
);

ALTER TABLE stage
ADD CONSTRAINT capacity_greater_than_zero CHECK(capacity>0)

CREATE TABLE performance(

	performance_id SERIAL PRIMARY KEY,
	performance_period TSRANGE NOT NULL,
	stage_id INT NOT NULL REFERENCES stage(stage_id),
	
	festival_performer_id INT NOT NULL REFERENCES festival_performer(festival_performer_id)
);

ALTER TABLE performance ADD CONSTRAINT no_overlapping_on_stage
	EXCLUDE USING gist(
		stage_id WITH=,
		performance_period WITH &&
	);


CREATE TYPE type_of_ticket AS ENUM ('jednodnevna','festivalska','VIP','kamp','promo');
CREATE TYPE ticket_validity AS ENUM('jedan_dan','cijeli_festival');

CREATE TABLE ticket_type(
	ticket_type_id SERIAL PRIMARY KEY,
	validity ticket_validity NOT NULL
);

CREATE TABLE ticket(
	ticket_id SERIAL PRIMARY KEY,
	ticket_type_id INT NOT NULL REFERENCES ticket_type(ticket_type_id),
	festival_id INT NOT NULL REFERENCES festival(festival_id) ON DELETE CASCADE
);

CREATE TABLE ticket_info(
	ticket_info_id SERIAL PRIMARY KEY,
	description TEXT,
	ticket_id INT NOT NULL UNIQUE REFERENCES ticket(ticket_id) ON DELETE CASCADE	
);

CREATE TABLE orders(
	order_id SERIAL PRIMARY KEY,
	amount INT NOT NULL,
	time_of_purchase TIMESTAMP NOT NULL,
	total_price NUMERIC NOT NULL,
	visitor_id INT NOT NULL REFERENCES visitor(visitor_id) ON DELETE SET NULL
	
);

CREATE TABLE order_item(
	order_item_id SERIAL PRIMARY KEY,
	price NUMERIC NOT NULL,
	quantity INT NOT NULL DEFAULT 1,
	order_id INT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
	ticket_id INT NOT NULL REFERENCES ticket(ticket_id)
	
);

CREATE TYPE staff_role AS ENUM ('organizator','tehnicar','zastitar','volonter');

CREATE TABLE staff(
	staff_id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	surname VARCHAR(30) NOT NULL,
	birth_date DATE,
	role staff_role NOT NULL,
	contact INT,
	has_safety_training BOOL NOT NULL,

	festival_id INT NOT NULL REFERENCES festival(festival_id)
);

ALTER TABLE staff
ADD CONSTRAINT check_age_of_guard
CHECK (role<> 'zastitar' OR EXTRACT(YEAR FROM AGE(birth_date))>=21);

ALTER TABLE staff
ALTER COLUMN has_safety_training SET DEFAULT FALSE;


CREATE TABLE festival_staff(
	festival_id INT NOT NULL REFERENCES festival(festival_id),
	staff_id INT NOT NULL REFERENCES staff(staff_id),
	festival_date DATERANGE,
	
	PRIMARY KEY(festival_id,staff_id)
);

ALTER TABLE festival_staff
ADD CONSTRAINT no_overlaping_festivals_for_staff
	EXCLUDE USING gist(
		staff_id WITH =,
		festival_date WITH &&
	);


CREATE TYPE membership_card_status AS ENUM('Aktivna','istekla');


CREATE TABLE membership_card(
	membership_card_id SERIAL PRIMARY KEY,
	date_of_activation DATE,
	status membership_card_status NOT NULL DEFAULT 'Aktivna',
	visitor_id INT NOT NULL REFERENCES visitor(visitor_id) ON DELETE CASCADE	
);


CREATE TYPE type_of_workshop AS ENUM('elektronička_glazba','klasicna_glazba','svjetlo_i_ton','DJ-ing','song-writing','marketing','produkcija','snimanje_zvuka');
CREATE TYPE workshop_difficulty AS ENUM('početna','srednja','napredna');

CREATE TABLE workshop(
	workshop_id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	capacity INT NOT NULL,
	type type_of_workshop,
	difficulty workshop_difficulty,
	duration INTERVAL NOT NULL,
	prior_knowledge_required BOOL,
	
	festival_id INT NOT NULL REFERENCES festival(festival_id)
);

ALTER TABLE workshop
ADD CONSTRAINT workshop_festival_unique UNIQUE (festival_id);


CREATE TYPE enrollment_status AS ENUM('prijavljen','otkazao','čeka_na_potvrdu','prisustvovao');

CREATE TABLE visitor_workshop(
	workshop_id INT NOT NULL REFERENCES workshop(workshop_id),
	visitor_id INT NOT NULL REFERENCES visitor(visitor_id),
	
	PRIMARY KEY(visitor_id,workshop_id),

	enrollment_time TIMESTAMP NOT NULL,
	status enrollment_status NOT NULL DEFAULT 'čeka_na_potvrdu'
);



