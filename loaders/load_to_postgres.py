import pandas as pd
import os
import sys

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import database connection string and gold layer path from config
from config import GOLD_PATH, POSTGRES_URI

def load_to_postgres():
    print("Loading gold layer to PostgreSQL...")
    
    # Read the final aggregated gold layer parquet file
    # This contains 31 rows — one per day with weather + trip stats
    df = pd.read_parquet(f"{GOLD_PATH}taxi_weather_gold.parquet")
    
    # Create a SQLAlchemy engine using the connection string from config
    # This connects to PostgreSQL running inside Docker
    from sqlalchemy import create_engine
    engine = create_engine(POSTGRES_URI)
    
    # Load dataframe into PostgreSQL table
    # if_exists="replace" drops and recreates the table on every run
    # This ensures fresh data every time the pipeline runs
    df.to_sql(
        "taxi_weather_analysis",  # table name in PostgreSQL
        engine,
        if_exists="replace",      # replace table if it already exists
        index=False               # don't write dataframe index as a column
    )
    
    print(f"Loaded {len(df)} rows to PostgreSQL")
    print("Done.")

# Only run this function when script is executed directly
# Not when it's imported by another script
if __name__ == "__main__":
    load_to_postgres()