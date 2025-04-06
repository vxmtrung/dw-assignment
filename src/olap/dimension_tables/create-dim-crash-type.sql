CREATE TABLE IF NOT EXISTS dim_crash_type (
  id SERIAL PRIMARY KEY,
  first_crash_type TEXT,
  crash_type TEXT,
  UNIQUE(first_crash_type, crash_type)
);