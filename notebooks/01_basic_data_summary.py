import pandas as pd

df = pd.read_csv(
    "data/processed/job_market_analytics_final_with_certificates.csv"
)

print("Dataset Shape:", df.shape)
print("\nData Info:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe(include="all"))
