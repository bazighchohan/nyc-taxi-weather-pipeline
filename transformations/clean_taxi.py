import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BRONZE_PATH, SILVER_PATH

def clean_taxi():
    print("Cleaning taxi data...")
    df = pd.read_parquet(f"{BRONZE_PATH}yellow_tripdata_2026-01.parquet")
    
    print(f"Rows before cleaning: {len(df)}")
    
    # Extract date from datetime
    df["date"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.date
    
    # Remove bad rows
    df = df[df["fare_amount"] > 0]
    df = df[df["trip_distance"] > 0]
    df = df[df["passenger_count"] > 0]
    df = df.dropna(subset=["tpep_pickup_datetime", "fare_amount"])
    
    # Keep only columns we need
    df = df[[
        "date",
        "tpep_pickup_datetime",
        "trip_distance",
        "passenger_count",
        "fare_amount",
        "total_amount",
        "payment_type"
    ]]
    
    print(f"Rows after cleaning: {len(df)}")

    # Quality checks
    assert len(df) > 0, "ERROR: No rows after cleaning"
    assert df["date"].isnull().sum() == 0, "ERROR: Null dates found"
    assert df["fare_amount"].min() > 0, "ERROR: Negative fares found"
    assert df["trip_distance"].min() > 0, "ERROR: Zero distance trips found"
    print("Quality checks passed ✓")

    
    df.to_parquet(f"{SILVER_PATH}taxi_clean.parquet", index=False)
    print(f"Saved to {SILVER_PATH}taxi_clean.parquet")

if __name__ == "__main__":
    clean_taxi()