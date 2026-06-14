import streamlit as st
import pandas as pd
import altair as alt
from groq import Groq
import os

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


st.set_page_config(layout="wide")
st.title("NYC Taxi Visualization System (GAP‑VizAI)")

@st.cache_data
def load_data():
    df = pd.read_csv("nyc_taxi_clean.csv")
    # Convert pickup datetime column (yellow taxi uses 'tpep_pickup_datetime')
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    # Rename payment_type codes to readable labels (optional)
    payment_map = {1: 'Credit Card', 2: 'Cash', 3: 'No Charge', 4: 'Dispute', 5: 'Unknown'}
    df['payment_type_label'] = df['payment_type'].map(payment_map).fillna('Other')
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("Chart Options")
chart_type = st.sidebar.selectbox("Select Chart", [
    "ECDF (Distance)",
    "Fare by Hour with CI",
    "Scatter Plot (Fare vs Distance)",
    "Treemap (Fare by Payment & Vendor)",      # NEW: composition
    "Violin Plot (Fare by Payment Type)"       # NEW: distribution
])
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

elif chart_type == "Scatter Plot (Fare vs Distance)":
    sample = df.sample(5000)
    scatter = alt.Chart(sample).mark_circle().encode(
        x='trip_distance:Q',
        y='fare_amount:Q',
        color=alt.Color('payment_type_label:N', scale=alt.Scale(scheme='category10'))
    ).properties(height=500).configure_mark(opacity=0.5)
    st.altair_chart(scatter, use_container_width=True)

elif chart_type == "Treemap (Fare by Payment & Vendor)":
    # Aggregate total fare by payment type and vendor
    treemap_data = df.groupby(['payment_type_label', 'VendorID'], as_index=False)['fare_amount'].sum()
    # Use a rectangular heatmap as a treemap alternative (Altair lacks native treemap)
    treemap = alt.Chart(treemap_data).mark_rect().encode(
        x='payment_type_label:N',
        y='VendorID:N',
        color=alt.Color('fare_amount:Q', scale=alt.Scale(scheme='yellowgreenblue')),
        tooltip=['payment_type_label', 'VendorID', 'fare_amount']
    ).properties(
        height=400,
        title="Total Fare Amount by Payment Type and Vendor"
    ).configure_view(strokeWidth=0)
    st.altair_chart(treemap, use_container_width=True)

elif chart_type == "Violin Plot (Fare by Payment Type)":
    # Altair doesn't have native violin, but density + area creates a similar effect
    # Limit fare to 0-100 for readability
    df_filtered = df[df['fare_amount'].between(0, 100)]
    violin = alt.Chart(df_filtered).transform_density(
        'fare_amount',
        as_=['fare_amount', 'density'],
        groupby=['payment_type_label'],
        extent=[0, 100]
    ).mark_area(orient='horizontal', opacity=0.7).encode(
        y=alt.Y('fare_amount:Q', title='Fare Amount ($)'),
        x=alt.X('density:Q', title='Density'),
        color=alt.Color('payment_type_label:N', scale=alt.Scale(scheme='category10'))
    ).properties(
        height=400,
        title='Distribution of Fare Amount by Payment Type (Violin-like)'
    )
    st.altair_chart(violin, use_container_width=True)

# AI Insight Generation
if use_ai:
    st.subheader("AI Insight")
    with st.spinner("Asking AI..."):
        # Load API key from environment variable (must be set)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            st.error("GROQ_API_KEY environment variable not set. Please set it to use AI insights.")
        else:
            client = Groq(api_key=api_key)
            # Provide a more specific prompt based on chart type
            prompt = f"""
            You are a data analyst. The current chart is a "{chart_type}" based on NYC taxi trip data.
            Write 2-3 sentences describing the main pattern, trend, or anomaly visible in this chart.
            Keep it concise and insightful.
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            st.write(response.choices[0].message.content)
# Add this after the AI Insight section
st.sidebar.divider()
if st.sidebar.button("🎯 Critique Current Chart"):
    st.subheader("AI Visualization Critique")
    with st.spinner("AI Critic evaluating..."):
        critique_prompt = f"""
        You are a visualization critic. Evaluate the "{chart_type}" chart for:
        1. Perceptual clarity (color choices, font size, layout) – score 1-10
        2. Encoding correctness (does the visual mapping match data types?) – score 1-10
        3. Uncertainty representation (are error bars/CI present and clear?) – score 1-10
        4. Accessibility (colorblind safe, sufficient contrast) – score 1-10
        Provide an overall score and 2-3 sentences of actionable feedback.
        """
        critique_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": critique_prompt}]
        )
        st.write(critique_response.choices[0].message.content)            