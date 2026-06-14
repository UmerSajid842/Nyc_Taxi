import streamlit as st
import pandas as pd
import altair as alt
from groq import Groq
import os

st.set_page_config(layout="wide")
st.title("NYC Taxi Visualization System (GAP‑VizAI)")

@st.cache_data
def load_data():
    df = pd.read_csv("nyc_taxi_clean.csv")
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("Chart Options")
chart_type = st.sidebar.selectbox("Select Chart", ["ECDF (Distance)", "Fare by Hour with CI", "Scatter Plot (Fare vs Distance)"])
use_ai = st.sidebar.checkbox("Generate AI Insight")

# Grammar-based chart generation
if chart_type == "ECDF (Distance)":
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('trip_distance:Q', title='Distance (miles)'),
        y=alt.Y('cumulative_count:Q', title='Cumulative Proportion', axis=alt.Axis(format='%')),
        color=alt.value('#1f77b4')
    ).transform_window(
        cumulative_count='count()', sort=[{'field': 'trip_distance'}]
    ).properties(height=500)
    st.altair_chart(chart, use_container_width=True)

elif chart_type == "Fare by Hour with CI":
    # Compute hourly means and CI (simplified for speed)
    hourly = df.groupby('hour')['fare_amount'].agg(['mean', 'sem']).reset_index()
    hourly['ci_low'] = hourly['mean'] - 1.96 * hourly['sem']
    hourly['ci_high'] = hourly['mean'] + 1.96 * hourly['sem']
    bars = alt.Chart(hourly).mark_bar(color='#2ca02c').encode(x='hour:O', y='mean:Q')
    errors = alt.Chart(hourly).mark_errorbar().encode(x='hour:O', y='ci_low:Q', y2='ci_high:Q')
    st.altair_chart(bars + errors, use_container_width=True)

else:
    sample = df.sample(5000)
    scatter = alt.Chart(sample).mark_circle().encode(
        x='trip_distance:Q', y='fare_amount:Q', color='payment_type:N'
    ).properties(height=500).configure_mark(opacity=0.5)
    st.altair_chart(scatter, use_container_width=True)

# AI Insight Generation
if use_ai:
    st.subheader("AI Insight")
    with st.spinner("Asking AI..."):
        client = Groq(api_key=os.environ.get("GROQ_API_KEY", "<REMOVED>"))
        prompt = f"Analyze the {chart_type} chart. The data shows taxi trips. Write 2-3 sentences describing the main pattern or anomaly."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response.choices[0].message.content)