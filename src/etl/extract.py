# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

def extract_csv():
  try:
      # Set the path to the file you'd like to load
      file_path = "traffic_accidents.csv"

      # Load the latest version
      df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "oktayrdeki/traffic-accidents",
        file_path,
        # Provide any additional arguments like 
        # sql_query or pandas_kwargs. See the 
        # documenation for more information:
        # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
        )
      print(f"Extract data successfully!")
      return df
  except Exception as e:
      print(f"Error reading CSV file: {e}")
      return None
    