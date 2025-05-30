import psycopg2
from config import DB_CONFIG
from pathlib import Path

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
      cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES %s ON CONFLICT DO NOTHING;", (tuple(row),))
      
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
        JOIN dim_traffic_control_device tc ON a.traffic_control_device = tc.traffic_control_device
        WHERE NOT EXISTS (
        SELECT 1 FROM fact_accidents f
        WHERE 
            f.date_id = d.id AND
            f.location_id = lo.id AND
            f.road_condition_id = rc.id AND
            f.weather_id = w.id AND
            f.lighting_id = li.id AND
            f.crash_type_id = c.id AND
            f.road_alignment_id = ra.id AND
            f.traffic_control_device_id = tc.id AND
            f.num_units = a.num_units AND
            f.most_severe_injury = a.most_severe_injury AND
            f.injuries_total = a.injuries_total AND
            f.injuries_fatal = a.injuries_fatal AND
            f.injuries_incapacitating = a.injuries_incapacitating AND
            f.injuries_non_incapacitating = a.injuries_non_incapacitating AND
            f.injuries_reported_not_evident = a.injuries_reported_not_evident AND
            f.injuries_no_indication = a.injuries_no_indication AND
            f.damage = a.damage AND
            f.prim_contributory_cause = a.prim_contributory_cause
        );
    """
    cursor.execute(query)
    
    print(f"Data successfully loaded into fact table!")

    conn.commit()
    conn.close()
  except Exception as e:
    print(f"Error loading data into fact table: {e}")

src_dir = Path(Path(__file__).resolve()).parents[1]

def create_data_table():
  with open(src_dir / "scripts" / "create-data-table.sql", "r") as f:
    sql = f.read()

  conn = psycopg2.connect(**DB_CONFIG)
  cursor = conn.cursor()
  
  cursor.execute(sql)
  conn.commit()

  conn.close()

def create_dim_tables():
  dim_tables_dir = src_dir / "olap" / "dimension_tables"

  conn = psycopg2.connect(**DB_CONFIG)
  cursor = conn.cursor()

  for sql_file in sorted(dim_tables_dir.glob("*.sql")):
    print(f"Executing {sql_file.name}")
    sql = sql_file.read_text()
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"✅ {sql_file.name} executed successfully.\n")
    except Exception as e:
        print(f"❌ Error executing {sql_file.name}: {e}\n")
        conn.rollback()
  
  conn.close()

def create_fact_tables():
  fact_tables_dir = src_dir / "olap" / "fact_tables"

  conn = psycopg2.connect(**DB_CONFIG)
  cursor = conn.cursor()

  for sql_file in sorted(fact_tables_dir.glob("*.sql")):
    print(f"Executing {sql_file.name}")
    sql = sql_file.read_text()
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"✅ {sql_file.name} executed successfully.\n")
    except Exception as e:
        print(f"❌ Error executing {sql_file.name}: {e}\n")
        conn.rollback()
  
  conn.close()