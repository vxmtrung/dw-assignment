CREATE TABLE IF NOT EXISTS dim_date (
  id SERIAL PRIMARY KEY,
  crash_date DATE UNIQUE,
  crash_hour INT,
  crash_day_of_week INT,
  crash_month INT
);