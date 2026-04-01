#!/bin/bash
set -e

echo "==============================="
echo "  NYC Taxi Pipeline Starting"
echo "==============================="

echo ""
echo "Step 1: Ingesting taxi data..."
python ingestion/ingest_taxi.py

echo ""
echo "Step 2: Ingesting weather data..."
python ingestion/ingest_weather.py

echo ""
echo "Step 3: Cleaning taxi data..."
python transformations/clean_taxi.py

echo ""
echo "Step 4: Cleaning weather data..."
python transformations/clean_weather.py

echo ""
echo "Step 5: Building gold layer..."
python transformations/join_and_aggregate.py

echo ""
echo "==============================="
echo "  Pipeline Complete"
echo "==============================="