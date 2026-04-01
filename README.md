# NYC Taxi + Weather Pipeline

A full end-to-end data engineering pipeline analyzing how weather affects NYC taxi demand and revenue.

## Business Question
**Do weather conditions affect NYC taxi trip volume and revenue?**

## Answer
Yes — clear days generate ~35% more revenue than snowy days. January 25, 2026 (33mm snowfall) saw trips drop to 19,000 — the lowest of the month.

## Live Dashboard
[View Dashboard](https://nyc-taxi-weather-pipeline-8ddskmisdp4m6pazyrwxss.streamlit.app/)

## Architecture
```
Raw Data → Bronze Layer → Silver Layer → Gold Layer → PostgreSQL → Streamlit
```

## Tech Stack
- Python + Pandas — ingestion and transformation
- PostgreSQL — data warehouse
- Docker — containerization
- Streamlit — dashboard and deployment
- Open-Meteo API — weather data
- NYC TLC — taxi trip records

## Pipeline Structure
```
nyc-taxi-weather-pipeline/
├── ingestion/          # data ingestion scripts
├── transformations/    # bronze → silver → gold
├── models/             # SQL schema
├── loaders/            # load to PostgreSQL
├── data/               # bronze, silver, gold layers
├── dashboard.py        # Streamlit dashboard
├── run_pipeline.sh     # orchestration script
└── docker-compose.yml  # PostgreSQL container
```

## How to Run
```bash
# Start PostgreSQL
sudo docker-compose up -d

# Activate virtual environment
source venv/bin/activate

# Run full pipeline
./run_pipeline.sh

# Launch dashboard
streamlit run dashboard.py
```

## Key Findings
- 2,551,845 trips analyzed across January 2026
- $73,792,021 total revenue
- Clear days: highest avg revenue (~$2.66M/day)
- Snowy days: lowest avg revenue (~$2.0M/day)
- Heaviest snow day (Jan 25): 81% fewer trips than avg clear day