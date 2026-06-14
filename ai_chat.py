import os
import re
from groq import Groq
import pandas as pd
import altair as alt

# -------- SET YOUR VALID API KEY HERE ---------
os.environ["GROQ_API_KEY"] = "<REMOVED>"
client = Groq()
# ---------------------------------------------

# Load data
df = pd.read_csv("nyc_taxi_clean.csv").sample(5000)

prompt = f"""
You are a data visualization expert. The dataset has columns: {list(df.columns)}.
Generate ONLY valid Altair Python code to create a scatter plot of 'fare_amount' vs 'trip_distance', colored by 'payment_type'. Use a colorblind‑safe palette (e.g., scheme='category10'). Do NOT include markdown backticks or any explanation. Output only raw Python code.
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

ai_code = response.choices[0].message.content
print("=== RAW AI CODE ===")
print(ai_code)

# Remove markdown code fences if present
ai_code_clean = re.sub(r'```python\s*|\s*```', '', ai_code).strip()
# Replace placeholder filename with actual CSV used in the notebook
ai_code_clean = ai_code_clean.replace('your_data.csv', 'nyc_taxi_clean.csv')
print("\n=== CLEAN CODE ===")
print(ai_code_clean)

# Execute safely
try:
    exec(ai_code_clean)
    if 'chart' in locals():
        chart.save('ai_scatter.html')
        chart.save('ai_scatter.png')
        print("Saved ai_scatter.html and ai_scatter.png")
    else:
        print("No 'chart' variable. Code executed but no chart saved.")
except Exception as e:
    print(f"Execution error: {e}")