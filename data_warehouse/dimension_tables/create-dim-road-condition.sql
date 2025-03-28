CREATE TABLE IF NOT EXISTS dim_road_condition (
  id SERIAL PRIMARY KEY,
  roadway_surface_cond TEXT,
  road_defect TEXT
);