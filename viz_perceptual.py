import altair as alt
import pandas as pd

df = pd.read_csv("nyc_taxi_clean.csv")

# Perceptually optimized ECDF
ecdf = alt.Chart(df).mark_line().encode(
    x=alt.X('trip_distance:Q', title='Trip Distance (miles)', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
    y=alt.Y('cumulative_count:Q', title='Cumulative Proportion', axis=alt.Axis(format='%', labelFontSize=12, titleFontSize=14)),
    color=alt.value('#1f77b4')  # colorblind‑safe blue
).transform_window(
    cumulative_count='count()',
    sort=[{'field': 'trip_distance'}]
).properties(
    title=alt.TitleParams('ECDF of Trip Distance', fontSize=18, anchor='start'),
    width=500,
    height=400
).configure_view(strokeWidth=0).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

ecdf.save('ecdf_perceptual.html')
ecdf.save('ecdf_perceptual.png')
print("Perceptually optimized ECDF saved.")