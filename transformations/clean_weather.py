import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BRONZE_PATH, SILVER_PATH

def clean_weather():
    print("Cleaning weather data...")
    df = pd.read_json(f"{BRONZE_PATH}weather_raw.json")
    
    print(f"Rows before cleaning: {len(df)}")
    
    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"]).dt.date
    
    # Remove any nulls
    df = df.dropna()
    
    # Add weather label based on weathercode
    def label_weather(code):
        if code in [0, 1]:
            return "clear"
        elif code in [2, 3]:
            return "cloudy"
        elif code in [51, 53, 55, 61, 63, 65]:
            return "rainy"
        elif code in [71, 73, 75, 77]:
            return "snowy"
        else:
            return "other"
    
    df["weather_label"] = df["weathercode"].apply(label_weather)
    
    print(f"Rows after cleaning: {len(df)}")
    print(df.head(5))

    # Quality checks
    assert len(df) > 0, "ERROR: No rows after cleaning"
    assert df["date"].isnull().sum() == 0, "ERROR: Null dates found"
    assert df["temp_max_c"].isnull().sum() == 0, "ERROR: Null temperatures found"
    assert df["weather_label"].isnull().sum() == 0, "ERROR: Null weather labels found"
    print("Quality checks passed ✓")
    
    df.to_parquet(f"{SILVER_PATH}weather_clean.parquet", index=False)
    print(f"Saved to {SILVER_PATH}weather_clean.parquet")

if __name__ == "__main__":
    clean_weather()