import pandas as pd

# For this example, we'll use the dataset from a teaching lab, which is a known, smaller sample of a single month.
# You can also replace this with a direct download link from the official NYC TLC portal.
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

print("Downloading NYC Taxi Data...")
df = pd.read_parquet(url)
print(f"Data loaded. Shape: {df.shape}")

# Data Cleaning: filter out unrealistic values for a clean analysis
df = df[
    (df['passenger_count'] > 0) &
    (df['trip_distance'] > 0) &
    (df['trip_distance'] <= 100) &
    (df['fare_amount'] > 0) &
    (df['fare_amount'] <= 500)
]

# Create a sample for faster processing, especially for initial testing
df_sample = df.sample(n=100000, random_state=42)
print(f"Data sampled. Shape: {df_sample.shape}")

# Save our clean, sampled data
df_sample.to_csv("nyc_taxi_clean.csv", index=False)
print("Data saved to nyc_taxi_clean.csv")