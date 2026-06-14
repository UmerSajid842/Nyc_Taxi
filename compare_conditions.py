import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

df = pd.read_csv("nyc_taxi_clean.csv").sample(5000)

# Condition A: Manual (Matplotlib default – no perceptual fixes)
plt.figure()
plt.scatter(df['trip_distance'], df['fare_amount'], c='blue', alpha=0.3)
plt.xlabel('Trip Distance')
plt.ylabel('Fare Amount')
plt.title('Condition A: Manual Chart')
plt.savefig('condition_A_manual.png')
plt.close()

# Condition B: Raw LLM output (simulated – no grammar constraints)
# This is what a naive LLM might generate without your pipeline
chart_b = alt.Chart(df).mark_circle().encode(
    x='trip_distance', y='fare_amount', color='payment_type'
).interactive()
chart_b.save('condition_B_llm_raw.png')

# Condition C: Your system (perceptual + grammar + uncertainty)
# Reuse your best chart from dashboard (e.g., scatter with colorblind palette)
chart_c = alt.Chart(df).mark_circle(opacity=0.5).encode(
    x=alt.X('trip_distance:Q', title='Distance (miles)'),
    y=alt.Y('fare_amount:Q', title='Fare ($)'),
    color=alt.Color('payment_type_label:N', scale=alt.Scale(scheme='category10'))
).properties(title='Condition C: GAP-VizAI System')
chart_c.save('condition_C_your_system.png')

print("All three condition charts saved.")

# figure4_combine_conditions.py
from PIL import Image
import os

# Load the three images
imgs = ['condition_A_manual.png', 'condition_B_llm_raw.png', 'condition_C_your_system.png']
images = [Image.open(img) for img in imgs]

# Get heights and widths (assume all same size)
widths, heights = zip(*(i.size for i in images))
total_width = sum(widths)
max_height = max(heights)

# Create new blank image
combined = Image.new('RGB', (total_width, max_height), color='white')

# Paste side by side
x_offset = 0
for img in images:
    combined.paste(img, (x_offset, 0))
    x_offset += img.width

combined.save('figure4_three_conditions.png')
print("Saved figure4_three_conditions.png")