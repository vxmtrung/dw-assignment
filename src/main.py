from etl.extract import extract_csv
from etl.transform import transform_data
from etl.load import load_to_db

def main():
  df = extract_csv("../data/raw/traffic_accidents.csv")
  df = transform_data(df)
  load_to_db(df, "raw_traffic_accidents")

if __name__ == "__main__":
    main()