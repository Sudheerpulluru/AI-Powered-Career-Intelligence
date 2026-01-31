import pandas as pd

df = pd.read_csv("data/processed/job_market_analytics_final_with_certificates.csv")

print("Shape:", df.shape)
print("Columns:", list(df.columns))
