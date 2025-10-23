-- remove old tables if they exist
DROP TABLE IF EXISTS customer_reservations;
DROP TABLE IF EXISTS hotel_booking;
DROP TABLE IF EXISTS all_bookings;

-- customer_reservations table
CREATE TABLE customer_reservations (
    booking_id TEXT NOT NULL,
    stays_in_weekend_nights INTEGER NOT NULL,
    stays_in_week_nights INTEGER NOT NULL,
    lead_time INTEGER NOT NULL,
    arrival_year INTEGER NOT NULL,
    arrival_month INTEGER NOT NULL,
    arrival_day INTEGER NOT NULL,
    market_segment_type TEXT NOT NULL,
    avg_price_per_room NUMERIC(10,2) NOT NULL,
    booking_status INTEGER NOT NULL
);

-- hotel_booking table
CREATE TABLE hotel_booking (
    hotel TEXT NOT NULL,
    booking_status INTEGER NOT NULL,
    lead_time INTEGER NOT NULL,
    arrival_year INTEGER NOT NULL,
    arrival_month INTEGER NOT NULL,
    arrival_date_week_number INTEGER NOT NULL,
    arrival_day INTEGER NOT NULL,
    stays_in_weekend_nights INTEGER NOT NULL,
    stays_in_week_nights INTEGER NOT NULL,
    market_segment_type TEXT NOT NULL,
    country TEXT NOT NULL,
    avg_price_per_room NUMERIC(10,2) NOT NULL,
    email TEXT NOT NULL
);

-- all_bookings table
CREATE TABLE all_bookings (
    stays_in_weekend_nights INTEGER NOT NULL,
    stays_in_week_nights INTEGER NOT NULL,
    lead_time INTEGER NOT NULL,
    arrival_year INTEGER NOT NULL,
    arrival_month INTEGER NOT NULL,
    arrival_day INTEGER NOT NULL,
    market_segment_type TEXT NOT NULL,
    avg_price_per_room NUMERIC(10,2) NOT NULL,
    booking_status INTEGER NOT NULL,
    email TEXT,
    booking_id TEXT
);

-- loading
COPY customer_reservations
FROM '/customer_reservations.csv'
DELIMITER ','
CSV HEADER;

COPY hotel_booking
FROM '/hotel_booking_cleaned.csv'
DELIMITER ','
CSV HEADER;

COPY all_bookings
FROM '/all_bookings.csv'
DELIMITER ','
CSV HEADER;