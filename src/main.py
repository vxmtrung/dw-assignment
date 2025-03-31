from etl.extract import extract_csv
from etl.transform import transform_data
from etl.load import load_to_db, distribute_data_to_dim_tables, distribute_data_to_fact_table

def main():
  df = extract_csv()
  df = transform_data(df)
  load_to_db(df, "raw_traffic_accidents")

  ### Heyy remember to run create .sql file first, i will write script for create real

  distribute_data_to_dim_tables()
  distribute_data_to_fact_table()

if __name__ == "__main__":
    main()