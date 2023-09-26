-- Users Table
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  username TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL  -- This would ideally be a hashed representation of the password
);

-- Codes Table
CREATE TABLE codes (
  code_id INTEGER PRIMARY KEY,
  code_value TEXT NOT NULL,  -- e.g., 'Available', 'In-use', 'Maintenance'
  comments TEXT
);

-- Modified Bikes Table
CREATE TABLE bikes (
  bike_id INTEGER PRIMARY KEY,
  bike_type TEXT,
  last_maintenance_date DATETIME,
  status_code INTEGER,
  comment TEXT,
  FOREIGN KEY (status_code) REFERENCES codes(code_id)
);


-- Maintenance Records Table
CREATE TABLE maintenance_records (
  maintenance_id INTEGER PRIMARY KEY,
  bike_id INTEGER,
  maintenance_date DATETIME,
  description TEXT,
  FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
);

--  Payment History Table that references the users and the trip_data table and keeps track of the amount paid for each trip

CREATE TABLE payment_history (
  payment_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  trip_index BIGINT,
  amount FLOAT,
  payment_date DATETIME,
  description TEXT,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (trip_index) REFERENCES trip_data(trip_index)
);

-- Bikeshare Stations Table (Provided by you)
CREATE TABLE bikeshare_stations (
  station_id INTEGER PRIMARY KEY,
  name TEXT,
  status TEXT,
  latitude FLOAT,
  longitude FLOAT
);

-- Trip Data Table that references the bikeshare_stations table and the users. and the bikes table

CREATE TABLE trip_data (
  trip_index BIGINT PRIMARY KEY,
  duration BIGINT,
  start_date DATETIME,
  end_date DATETIME,
  start_station BIGINT,
  end_station BIGINT,
  bike_id INTEGER,
  user_id INTEGER,
  FOREIGN KEY (start_station) REFERENCES bikeshare_stations(station_id),
  FOREIGN KEY (end_station) REFERENCES bikeshare_stations(station_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
);

-- Payment Types Table that  is a lookup table for the different types of payment types that a user can have
CREATE TABLE payment_types (
  payment_type_id INTEGER PRIMARY KEY,
  type_name TEXT NOT NULL  -- e.g., 'Credit Card', 'PayPal', 'Debit Card'
);

--mapping table for the user and the payment types. This keeps track of the payment types that a user has done
CREATE TABLE user_payment_types (
  user_id INTEGER,
  payment_type_id INTEGER,
  PRIMARY KEY (user_id, payment_type_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (payment_type_id) REFERENCES payment_types(payment_type_id)
);
