CREATE TABLE IF NOT EXISTS fact_accidents (
  id SERIAL PRIMARY KEY,
  date_id INT REFERENCES dim_date(id),
  location_id INT REFERENCES dim_location(id),
  road_condition_id INT REFERENCES dim_road_condition(id),
  weather_id INT REFERENCES dim_weather(id),
  lighting_id INT REFERENCES dim_lighting(id),
  crash_type_id INT REFERENCES dim_crash_type(id),
  road_alignment_id INT REFERENCES dim_road_alignment(id),
  traffic_control_device_id INT REFERENCES dim_traffic_control_device(id),
  num_units INT,
  most_severe_injury TEXT,
  injuries_total INT,
  injuries_fatal INT,
  injuries_incapacitating INT,
  injuries_non_incapacitating INT,
  injuries_reported_not_evident INT,
  injuries_no_indication INT,
  damage TEXT,
  prim_contributory_cause TEXT
);