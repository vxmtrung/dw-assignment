import pandas as pd

def transform_data(df):
    df.dropna(inplace=True)
    df['crash_date'] = pd.to_datetime(df['crash_date'], format='%m/%d/%Y %I:%M:%S %p')
    return df