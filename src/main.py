from etl.extract import extract_csv
from etl.transform import transform_data
from etl.load import load_to_db, distribute_data_to_dim_tables, distribute_data_to_fact_table, create_data_table, create_dim_tables, create_fact_tables

def main():
  df = extract_csv()
  df = transform_data(df)

  create_data_table()
  create_dim_tables()
  create_fact_tables()
  
  load_to_db(df, "raw_traffic_accidents")

  distribute_data_to_dim_tables()
  distribute_data_to_fact_table()

if __name__ == "__main__":
    main()