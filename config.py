import os
from dotenv import load_dotenv

load_dotenv()

# Database
POSTGRES_USER     = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB       = os.getenv("POSTGRES_DB")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT")

POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Layer paths
BRONZE_PATH = "data/bronze/"
SILVER_PATH = "data/silver/"
GOLD_PATH   = "data/gold/"