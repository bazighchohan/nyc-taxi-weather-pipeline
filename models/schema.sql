CREATE TABLE IF NOT EXISTS taxi_weather_analysis (
    date              DATE,
    weather_label     VARCHAR(20),
    temp_max_c        FLOAT,
    precipitation_mm  FLOAT,
    total_trips       INT,
    avg_fare          FLOAT,
    avg_distance      FLOAT,
    total_revenue     FLOAT
);