import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NYC Taxi + Weather Analysis", layout="wide")

st.title("NYC Taxi + Weather Pipeline")
st.markdown("**Business question:** Does weather affect NYC taxi demand and revenue?")

df = pd.read_csv("data/gold/taxi_weather_gold.csv")
df["date"] = pd.to_datetime(df["date"])

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trips", f"{df['total_trips'].sum():,}")
col2.metric("Total Revenue", f"${df['total_revenue'].sum():,.0f}")
col3.metric("Avg Daily Trips", f"{df['total_trips'].mean():,.0f}")
col4.metric("Days Analyzed", len(df))

st.divider()

# Chart 1 - Daily trips
st.subheader("Daily Trips — January 2026")
fig1 = px.bar(df, x="date", y="total_trips", color="weather_label",
              title="Daily Trips Colored by Weather Condition",
              labels={"total_trips": "Total Trips", "date": "Date", "weather_label": "Weather"},
              color_discrete_map={"clear": "#FFD700", "cloudy": "#A9A9A9", "rainy": "#4169E1", "snowy": "#00BFFF"})
fig1.update_traces(width=60000000)
st.plotly_chart(fig1, use_container_width=True)
st.caption("📌 January 25 shows a dramatic drop to ~19,000 trips — that day had 33mm of precipitation (heaviest snowfall of the month). Clear days consistently show higher trip counts than snowy days.")

st.divider()

# Chart 2 - Revenue by weather
st.subheader("Average Revenue by Weather Condition")
weather_summary = df.groupby("weather_label").agg(
    avg_revenue=("total_revenue", "mean"),
    avg_trips=("total_trips", "mean"),
    days=("date", "count")
).reset_index()

fig2 = px.bar(weather_summary, x="weather_label", y="avg_revenue",
              color="weather_label", title="Avg Daily Revenue by Weather",
              labels={"avg_revenue": "Avg Daily Revenue ($)", "weather_label": "Weather Condition"},
              color_discrete_map={"clear": "#FFD700", "cloudy": "#A9A9A9", "rainy": "#4169E1", "snowy": "#00BFFF"},
              text="avg_revenue")
fig2.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
st.plotly_chart(fig2, use_container_width=True)
st.caption("📌 Clear days generate ~35% more revenue than snowy days. Rainy days surprisingly perform well — possibly because people avoid walking and take more taxis.")

st.divider()

# Chart 3 - Trips by temperature bins
st.subheader("Trips vs Temperature")
df["temp_bin"] = pd.cut(df["temp_max_c"],
                         bins=[-15, -5, 0, 5, 10, 15],
                         labels=["< -5°C", "-5 to 0°C", "0 to 5°C", "5 to 10°C", "10 to 15°C"])
temp_summary = df.groupby("temp_bin", observed=True).agg(
    avg_trips=("total_trips", "mean")
).reset_index()

fig3 = px.bar(temp_summary, x="temp_bin", y="avg_trips",
              title="Average Trips by Temperature Range",
              labels={"temp_bin": "Temperature Range", "avg_trips": "Avg Daily Trips"},
              color="avg_trips", color_continuous_scale="Blues")
fig3.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
st.plotly_chart(fig3, use_container_width=True)
st.caption("📌 The relationship between temperature and trips is not strictly linear — extremely cold days still see high trip counts, likely because people avoid walking in freezing weather.")

st.divider()

st.markdown("**Data sources:** NYC TLC Trip Records + Open-Meteo Weather API | **Pipeline:** Python → Pandas → PostgreSQL → Docker → Streamlit")