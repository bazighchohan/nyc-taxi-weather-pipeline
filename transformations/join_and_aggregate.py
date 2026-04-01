import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SILVER_PATH, GOLD_PATH

def build_gold():
    print("Building gold layer...")
    
    taxi    = pd.read_parquet(f"{SILVER_PATH}taxi_clean.parquet")
    weather = pd.read_parquet(f"{SILVER_PATH}weather_clean.parquet")
    
    # JOIN on date
    merged = taxi.merge(weather, on="date", how="left")
    print(f"Merged rows: {len(merged)}")
    
    # Aggregate by date + weather
    gold = merged.groupby(["date", "weather_label", "temp_max_c", "precipitation_mm"]).agg(
        total_trips   = ("fare_amount", "count"),
        avg_fare      = ("fare_amount", "mean"),
        avg_distance  = ("trip_distance", "mean"),
        total_revenue = ("total_amount", "sum")
    ).reset_index()
    
    gold["avg_fare"]      = gold["avg_fare"].round(2)
    gold["avg_distance"]  = gold["avg_distance"].round(2)
    gold["total_revenue"] = gold["total_revenue"].round(2)
    
    print(f"Gold rows: {len(gold)}")
    print(gold.head(10))
    
    gold.to_parquet(f"{GOLD_PATH}taxi_weather_gold.parquet", index=False)
    print(f"Saved to {GOLD_PATH}taxi_weather_gold.parquet")

if __name__ == "__main__":
    build_gold()