import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BRONZE_PATH

def ingest_taxi():
    print("Loading taxi data...")
    df = pd.read_parquet(f"{BRONZE_PATH}yellow_tripdata_2026-01.parquet")
    
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))

if __name__ == "__main__":
    ingest_taxi()