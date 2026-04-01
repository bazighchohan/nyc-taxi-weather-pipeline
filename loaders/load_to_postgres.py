import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GOLD_PATH, POSTGRES_URI

def load_to_postgres():
    print("Loading gold layer to PostgreSQL...")
    
    df = pd.read_parquet(f"{GOLD_PATH}taxi_weather_gold.parquet")
    
    from sqlalchemy import create_engine
    engine = create_engine(POSTGRES_URI)
    
    df.to_sql(
        "taxi_weather_analysis",
        engine,
        if_exists="replace",
        index=False
    )
    
    print(f"Loaded {len(df)} rows to PostgreSQL")
    print("Done.")

if __name__ == "__main__":
    load_to_postgres()