import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

# Load your cleaned data
df = pd.read_csv("nyc_taxi_clean.csv").sample(5000)

# ----- Condition A: Manual chart (Matplotlib, no fixes) -----
plt.figure(figsize=(6,4))
plt.scatter(df['trip_distance'], df['fare_amount'], c='blue', alpha=0.3)
plt.xlabel('Trip Distance (miles)')
plt.ylabel('Fare Amount ($)')
plt.title('Manual Chart (Condition A)')
plt.savefig('condition_A_manual.png', dpi=150)
plt.close()

# ----- Condition B: Raw LLM output (simulated naive code) -----
chart_b = alt.Chart(df).mark_circle().encode(
    x='trip_distance',          # missing :Q
    y='fare_amount',            # missing :Q
    color='payment_type'        # no colorblind palette
).interactive()
chart_b.save('condition_B_llm_raw.png')

# ----- Condition C: Your GAP-VizAI system (perceptual + grammar) -----
chart_c = alt.Chart(df).mark_circle(opacity=0.5).encode(
    x=alt.X('trip_distance:Q', title='Distance (miles)'),
    y=alt.Y('fare_amount:Q', title='Fare ($)'),
    color=alt.Color('payment_type_label:N', scale=alt.Scale(scheme='category10'))
).properties(title='GAP‑VizAI (Condition C)', height=400, width=500)
chart_c.save('condition_C_your_system.png')

print("Saved: condition_A_manual.png, condition_B_llm_raw.png, condition_C_your_system.png")