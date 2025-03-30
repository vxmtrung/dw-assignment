import psycopg2
from config import DB_CONFIG

def load_to_db(df, table_name):
  try:
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
      
    print(f"Data successfully loaded into table {table_name}!")
    
    conn.commit()
    conn.close()
  
  except Exception as e:
    print(f"Error loading data into table {table_name}!")

def distribute_data_to_dim_tables():
  try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    queries = [
      """
        INSERT INTO dim_date (crash_date, crash_hour, crash_day_of_week, crash_month)
        SELECT DISTINCT crash_date, crash_hour, crash_day_of_week, crash_month
        FROM raw_traffic_accidents
        ON CONFLICT (crash_date) DO NOTHING;
      """,
      """
        INSERT INTO dim_crash_type (first_crash_type, crash_type)
        SELECT DISTINCT first_crash_type, crash_type
        FROM raw_traffic_accidents
        ON CONFLICT (first_crash_type, crash_type) DO NOTHING;
      """,
      """
        INSERT INTO dim_lighting (lighting_condition)
        SELECT DISTINCT lighting_condition
        FROM raw_traffic_accidents
        ON CONFLICT (lighting_condition) DO NOTHING;
      """,
      """
        INSERT INTO dim_location (intersection_related, trafficway_type)
        SELECT DISTINCT intersection_related, trafficway_type
        FROM raw_traffic_accidents
        ON CONFLICT (intersection_related, trafficway_type) DO NOTHING;
      """,
      """
        INSERT INTO dim_road_alignment (alignment)
        SELECT DISTINCT alignment
        FROM raw_traffic_accidents
        ON CONFLICT (alignment) DO NOTHING;
      """,
      """
        INSERT INTO dim_road_condition (roadway_surface_cond, road_defect)
        SELECT DISTINCT roadway_surface_cond, road_defect
        FROM raw_traffic_accidents
        ON CONFLICT (roadway_surface_cond, road_defect) DO NOTHING;
      """,
      """
        INSERT INTO dim_traffic_control_device (traffic_control_device)
        SELECT DISTINCT traffic_control_device
        FROM raw_traffic_accidents
        ON CONFLICT (traffic_control_device) DO NOTHING;
      """,
      """
        INSERT INTO dim_weather (weather_condition)
        SELECT DISTINCT weather_condition
        FROM raw_traffic_accidents
        ON CONFLICT (weather_condition) DO NOTHING;
      """
    ]

    for query in queries:
      cursor.execute(query)
      
    print(f"Data successfully loaded into dim tables!")

    conn.commit()
    conn.close()
  except Exception as e:
    print(f"Error loading data into dim tables: {e}")

def distribute_data_to_fact_table():
  try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    query = """
      INSERT INTO fact_accidents (date_id, location_id, road_condition_id, weather_id, lighting_id, crash_type_id, road_alignment_id, traffic_control_device_id,
      num_units, most_severe_injury, injuries_total, injuries_fatal, injuries_incapacitating, injuries_non_incapacitating, injuries_reported_not_evident, injuries_no_indication,
      damage, prim_contributory_cause)
      SELECT 
        d.id,
        lo.id,
        rc.id,
        w.id,
        li.id,
        c.id,
        ra.id,
        tc.id,
        a.num_units,
        a.most_severe_injury,
        a.injuries_total,
        a.injuries_fatal,
        a.injuries_incapacitating,
        a.injuries_non_incapacitating,
        a.injuries_reported_not_evident,
        a.injuries_no_indication,
        a.damage,
        a.prim_contributory_cause
        FROM raw_traffic_accidents a
        JOIN dim_date d ON a.crash_date::DATE = d.crash_date
        JOIN dim_location lo ON a.intersection_related = lo.intersection_related AND a.trafficway_type = lo.trafficway_type
        JOIN dim_road_condition rc ON a.roadway_surface_cond = rc.roadway_surface_cond AND a.road_defect = rc.road_defect
        JOIN dim_weather w ON a.weather_condition = w.weather_condition
        JOIN dim_lighting li ON a.lighting_condition = li.lighting_condition
        JOIN dim_crash_type c ON a.first_crash_type = c.first_crash_type AND a.crash_type = c.crash_type
        JOIN dim_road_alignment ra ON a.alignment = ra.alignment
        JOIN dim_traffic_control_device tc ON a.traffic_control_device = tc.traffic_control_device;
    """
    cursor.execute(query)
    
    print(f"Data successfully loaded into fact table!")

    conn.commit()
    conn.close()
  except Exception as e:
    print(f"Error loading data into fact table: {e}")


