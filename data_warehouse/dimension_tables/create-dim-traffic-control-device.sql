CREATE TABLE IF NOT EXISTS dim_traffic_control_device (
  id SERIAL PRIMARY KEY,
  traffic_control_device TEXT UNIQUE
);