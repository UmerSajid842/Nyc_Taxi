# figure6_uncertainty_examples.py
import pandas as pd
import altair as alt

df = pd.read_csv("nyc_taxi_clean.csv")
df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['hour'] = df['pickup_datetime'].dt.hour

# 1. Bar chart with 95% CI
hourly = df.groupby('hour')['fare_amount'].agg(['mean', 'sem']).reset_index()
hourly['ci_low'] = hourly['mean'] - 1.96 * hourly['sem']
hourly['ci_high'] = hourly['mean'] + 1.96 * hourly['sem']
bars = alt.Chart(hourly).mark_bar(color='#2ca02c').encode(x='hour:O', y='mean:Q')
errors = alt.Chart(hourly).mark_errorbar().encode(x='hour:O', y='ci_low:Q', y2='ci_high:Q')
chart_ci = (bars + errors).properties(title='Mean Fare by Hour with 95% CI', width=400)

# 2. Violin-like density plot
df_filtered = df[df['fare_amount'].between(0, 100)].copy()
df_filtered['payment_type_label'] = df_filtered['payment_type'].map({1:'Credit',2:'Cash'})
violin = alt.Chart(df_filtered).transform_density(
    'fare_amount',
    as_=['fare_amount', 'density'],
    groupby=['payment_type_label'],
    extent=[0,100]
).mark_area(orient='horizontal', opacity=0.7).encode(
    y=alt.Y('fare_amount:Q', title='Fare ($)'),
    x=alt.X('density:Q', title='Density'),
    color=alt.Color('payment_type_label:N', scale=alt.Scale(scheme='category10'))
).properties(title='Fare Distribution by Payment Type', width=400)

# Combine side by side
combined_uncertainty = alt.hconcat(chart_ci, violin)
combined_uncertainty.save('figure6_uncertainty_examples.png')
print("Saved figure6_uncertainty_examples.png")