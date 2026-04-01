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

# Chart 1 - Daily trips over time
st.subheader("Daily Trips — January 2026")
fig1 = px.bar(df, x="date", y="total_trips", color="weather_label",
              title="Daily Trips Colored by Weather Condition",
              color_discrete_map={
                  "clear": "#FFD700",
                  "cloudy": "#A9A9A9",
                  "rainy": "#4169E1",
                  "snowy": "#00BFFF"
              })
fig1.update_layout(showlegend=True)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Revenue by weather
st.subheader("Average Revenue by Weather Condition")
weather_summary = df.groupby("weather_label").agg(
    avg_revenue=("total_revenue", "mean"),
    avg_trips=("total_trips", "mean")
).reset_index()

fig2 = px.bar(weather_summary, x="weather_label", y="avg_revenue",
              color="weather_label", title="Avg Daily Revenue by Weather")
st.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Trips vs temperature
st.subheader("Trips vs Temperature")
fig3 = px.scatter(df, x="temp_max_c", y="total_trips", color="weather_label",
                  size="total_revenue", hover_data=["date"],
                  title="Do warmer days mean more trips?")
st.plotly_chart(fig3, use_container_width=True)

st.caption("Data: NYC TLC + Open-Meteo | Pipeline: Python, Pandas, PostgreSQL, Docker")