import requests
import pandas as pd
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BRONZE_PATH

def ingest_weather(start_date="2026-01-01", end_date="2026-01-31"):
    print("Fetching weather data from Open-Meteo...")
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "daily": "temperature_2m_max,precipitation_sum,weathercode",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "America/New_York"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp_max_c": data["daily"]["temperature_2m_max"],
        "precipitation_mm": data["daily"]["precipitation_sum"],
        "weathercode": data["daily"]["weathercode"]
    })
    
    df["date"] = pd.to_datetime(df["date"])
    
    output_path = f"{BRONZE_PATH}weather_raw.json"
    df.to_json(output_path, orient="records", indent=2, date_format="iso")
    
    print(f"Rows: {len(df)}")
    print(df.head(5))
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    ingest_weather()