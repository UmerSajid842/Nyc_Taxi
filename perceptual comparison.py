# figure3_perceptual_comparison.py
import pandas as pd
import altair as alt

df = pd.read_csv("nyc_taxi_clean.csv").sample(5000)

# Before optimization (default Altair)
chart_before = alt.Chart(df).mark_circle().encode(
    x='trip_distance:Q',
    y='fare_amount:Q',
    color='payment_type:N'
).properties(
    title="Before: Default Palette + Grid",
    width=300,
    height=300
)

# After optimization (category10, no grid)
chart_after = alt.Chart(df).mark_circle().encode(
    x=alt.X('trip_distance:Q', title='Distance (miles)', axis=alt.Axis(grid=False)),
    y=alt.Y('fare_amount:Q', title='Fare ($)', axis=alt.Axis(grid=False)),
    color=alt.Color('payment_type_label:N', scale=alt.Scale(scheme='category10'))
).properties(
    title="After: Colorblind-safe + No Grid",
    width=300,
    height=300
)

# Combine side by side
combined = alt.hconcat(chart_before, chart_after).resolve_scale(
    color='independent'
).configure_view(
    strokeWidth=0
)
combined.save('figure3_perceptual_comparison.png')
print("Saved figure3_perceptual_comparison.png")