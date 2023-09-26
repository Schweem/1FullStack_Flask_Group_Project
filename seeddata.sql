-- Insert sample data into the 'users' table
INSERT INTO users (username, email, password) VALUES
  ('user1', 'user1@example.com', 'password1'),
  ('user2', 'user2@example.com', 'password2'),
  ('user3', 'user3@example.com', 'password3');

-- Insert sample data into the 'codes' table
INSERT INTO codes (code_value, comments) VALUES
  ('Available', 'Bike is available for use'),
  ('In-use', 'Bike is currently in use'),
  ('Maintenance', 'Bike is under maintenance');

-- Insert sample data into the 'bikes' table
INSERT INTO bikes (bike_type, last_maintenance_date, status_code, comment) VALUES
  ('Mountain Bike', '2023-09-20 10:30:00', 1, 'No issues'),
  ('Road Bike', '2023-09-19 14:45:00', 2, 'In use by user1'),
  ('Hybrid Bike', '2023-09-18 09:15:00', 3, 'Scheduled maintenance');

-- Insert sample data into the 'maintenance_records' table
INSERT INTO maintenance_records (bike_id, maintenance_date, description) VALUES
  (1, '2023-09-19 09:00:00', 'Routine checkup'),
  (3, '2023-09-17 15:30:00', 'Replace brake pads');

-- Insert sample data into the 'payment_history' table
INSERT INTO payment_history (user_id, trip_index, amount, payment_date, description) VALUES
  (1, 1, 5.99, '2023-09-21 14:00:00', 'Trip payment'),
  (2, 2, 7.49, '2023-09-20 09:30:00', 'Trip payment'),
  (3, 3, 4.99, '2023-09-19 17:45:00', 'Trip payment');

-- Insert sample data into the 'bikeshare_stations' table
INSERT INTO bikeshare_stations (name, status, latitude, longitude) VALUES
  ('Station A', 'Active', 40.7128, -74.0060),
  ('Station B', 'Active', 34.0522, -118.2437),
  ('Station C', 'Maintenance', 41.8781, -87.6298);

-- Insert sample data into the 'trip_data' table
INSERT INTO trip_data (trip_index, duration, start_date, end_date, start_station, end_station, bike_id, user_id) VALUES
  (1, 30, '2023-09-21 13:00:00', '2023-09-21 13:30:00', 1, 2, 1, 1),
  (2, 45, '2023-09-20 08:45:00', '2023-09-20 09:30:00', 2, 1, 2, 2),
  (3, 25, '2023-09-19 17:00:00', '2023-09-19 17:25:00', 3, 1, 3, 3);

-- Insert sample data into the 'payment_types' table
INSERT INTO payment_types (type_name) VALUES
  ('Credit Card'),
  ('PayPal'),
  ('Debit Card');
--
-- -- Insert sample data into the 'user_payment_types' table
-- INSERT INTO user_payment_types (user_id, payment_type_id) VALUES
--   (1, 1),
--   (2, 2),
--   (3, 3);
