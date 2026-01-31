import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/indian_jobs.csv")

# Convert date
df["postdate"] = pd.to_datetime(df["postdate"], errors="coerce")
df = df.dropna(subset=["postdate"])

# Monthly trend
trend = df.groupby(df["postdate"].dt.to_period("M")).size()

# Plot
plt.figure(figsize=(10,5))
trend.plot()
plt.title("Job Market Trend Over Time (India)")
plt.xlabel("Time")
plt.ylabel("Number of Job Postings")
plt.grid(True)

plt.savefig("results/job_trend.png")
plt.show()
cities = ["bangalore", "hyderabad", "pune", "chennai", "mumbai", "delhi"]

df["joblocation_address"] = df["joblocation_address"].fillna("").str.lower()

plt.figure(figsize=(10,5))

for city in cities:
    city_df = df[df["joblocation_address"].str.contains(city)]
    city_trend = city_df.groupby(city_df["postdate"].dt.to_period("M")).size()
    city_trend.plot(label=city.capitalize())

plt.title("City-wise Job Demand Trend")
plt.xlabel("Time")
plt.ylabel("Number of Jobs")
plt.legend()
plt.grid(True)

plt.savefig("results/city_trend.png")
plt.show()
skills = ["python", "java", "sql", "machine learning"]

plt.figure(figsize=(10,5))

for skill in skills:
    skill_df = df[df["skills"].fillna("").str.lower().str.contains(skill)]
    skill_trend = skill_df.groupby(skill_df["postdate"].dt.to_period("M")).size()
    skill_trend.plot(label=skill.capitalize())

plt.title("Skill Demand Trend Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Jobs")
plt.legend()
plt.grid(True)

plt.savefig("results/skill_trend.png")
plt.show()
