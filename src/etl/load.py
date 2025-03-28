import psycopg2
from config import DB_CONFIG

def load_to_db(df, table_name):
  conn = psycopg2.connect(**DB_CONFIG)
  cursor = conn.cursor()
  columns = """
    crash_date, traffic_control_device, weather_condition, lighting_condition,
    first_crash_type, trafficway_type, alignment, roadway_surface_cond, road_defect,
    crash_type, intersection_related, damage, prim_contributory_cause, num_units,
    most_severe_injury, injuries_total, injuries_fatal, injuries_incapacitating,
    injuries_non_incapacitating, injuries_reported_not_evident, injuries_no_indication,
    crash_hour, crash_day_of_week, crash_month
"""
  for _, row in df.iterrows():
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES %s", (tuple(row),))
    print(f"Executed query: INSERT INTO {table_name} ({columns}) VALUES %s")
  
  conn.commit()
  conn.close()