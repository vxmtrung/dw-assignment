import pandas as pd

def transform_data(df):
    try:
        df.dropna(inplace=True)
        df['crash_date'] = pd.to_datetime(df['crash_date'], format='%m/%d/%Y %I:%M:%S %p')
        df.dropna(subset=['crash_date'], inplace=True)
        df.drop_duplicates(inplace=True)
        print(f"Transform data successfully!")
        return df
    except Exception as e:
        print(f"Error processing data: {e}")
        return None