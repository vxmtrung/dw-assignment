CREATE TABLE IF NOT EXISTS dim_location (
  id SERIAL PRIMARY KEY,
  intersection_related BOOLEAN,
  trafficway_type BOOLEAN
);