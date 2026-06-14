import altair as alt
import pandas as pd

# Load the cleaned data
df = pd.read_csv("nyc_taxi_clean.csv")

# Simple ECDF of trip distance
ecdf_plot = alt.Chart(df).mark_line().encode(
    x='trip_distance:Q',
    y='cumulative_count:Q'
).transform_window(
    cumulative_count='count()',
    sort=[{'field': 'trip_distance'}]
).properties(
    title='ECDF of Trip Distance (NYC Taxi)',
    width=600,
    height=400
)

# Save as HTML and PNG
ecdf_plot.save('ecdf_plot.html')
ecdf_plot.save('ecdf_plot.png')
print("ECDF plot saved as 'ecdf_plot.html' and 'ecdf_plot.png'")

# To display the plot if you're in a Jupyter notebook environment:
# ecdf_plot.show()