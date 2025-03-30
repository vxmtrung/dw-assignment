import pandas as pd

def extract_csv(file_path):
  try:
      df = pd.read_csv(file_path)
      print(f"Extract data successfully!")
      return df
  except Exception as e:
      print(f"Error reading CSV file: {e}")
      return None
    