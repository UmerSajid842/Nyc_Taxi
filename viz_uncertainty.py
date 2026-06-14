import altair as alt
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("nyc_taxi_clean.csv")

# Extract hour of day from pickup datetime (convert to datetime first)
df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['hour'] = df['pickup_datetime'].dt.hour

# Compute mean fare and 95% CI per hour
def mean_ci(x):
    mean = np.mean(x)
    ci = stats.t.interval(0.95, len(x)-1, loc=mean, scale=stats.sem(x))
    return pd.Series({'mean': mean, 'ci_low': ci[0], 'ci_high': ci[1]})

hourly = df.groupby('hour')['fare_amount'].apply(mean_ci).unstack().reset_index()

# Bar chart with error bars (confidence intervals)
bars = alt.Chart(hourly).mark_bar(color='#2ca02c').encode(
    x='hour:O',
    y='mean:Q'
)

errors = alt.Chart(hourly).mark_errorbar(color='black').encode(
    x='hour:O',
    y='ci_low:Q',
    y2='ci_high:Q'
)

chart = (bars + errors).properties(
    title='Mean Fare Amount by Hour of Day with 95% CI',
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

chart.save('uncertainty_bars.html')
chart.save('uncertainty_bars.png')
print("Uncertainty visualization saved.")