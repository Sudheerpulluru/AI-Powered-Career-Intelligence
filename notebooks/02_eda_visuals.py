import pandas as pd
import matplotlib.pyplot as plt
import os

# ===============================
# LOAD CLEAN DATA
# ===============================
DATA_PATH = "data/processed/job_market_clean.csv"
df = pd.read_csv(DATA_PATH)

# Create output folder
os.makedirs("results/plots", exist_ok=True)

# ===============================
# 1. JOB TITLE DISTRIBUTION
# ===============================
plt.figure()
df["job_title"].value_counts().head(10).plot(kind="bar")
plt.title("Top Job Roles Distribution")
plt.xlabel("Job Role")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/plots/job_role_distribution.png")
plt.close()

# ===============================
# 2. LOCATION DISTRIBUTION
# ===============================
plt.figure()
df["location"].value_counts().head(10).plot(kind="bar")
plt.title("Top Job Locations")
plt.xlabel("Location")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/plots/location_distribution.png")
plt.close()

# ===============================
# 3. DEMAND LABEL DISTRIBUTION
# ===============================
plt.figure()
df["demand_label"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Job Demand Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("results/plots/demand_distribution.png")
plt.close()

print("EDA visuals generated and saved in results/plots/")
