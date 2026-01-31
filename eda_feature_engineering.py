import pandas as pd
import os
import joblib

# 🔧 Disable GUI backend (prevents Tkinter issues)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ===============================
# PROJECT ROOT
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ===============================
# PATHS
# ===============================
DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data", "processed",
    "job_market_analytics_final_with_certificates.csv"
)

OUTPUT_PATH = os.path.join(
    PROJECT_ROOT,
    "data", "processed",
    "job_market_features_engineered.csv"
)

print("📂 Using MAIN dataset:")
print(DATA_PATH)

# ===============================
# LOAD DATASET
# ===============================
if not os.path.exists(DATA_PATH):
    print("❌ Dataset not found!")
    exit(1)

df = pd.read_csv(DATA_PATH)
df.fillna("Unknown", inplace=True)

# Normalize column names
df.columns = [c.lower() for c in df.columns]

print("✅ Dataset loaded:", df.shape)

# ===============================
# ---------- BASIC EDA ----------
# ===============================
os.makedirs("results", exist_ok=True)

# Demand distribution
plt.figure()
df["demand_label"].value_counts().plot(kind="bar")
plt.title("Job Demand Distribution")
plt.xlabel("Demand Level")
plt.ylabel("Count")
plt.savefig("results/demand_distribution.png")
plt.close()

# Top industries
plt.figure()
df["industry"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Industries")
plt.savefig("results/top_industries.png")
plt.close()

# Top locations
plt.figure()
df["location"].value_counts().head(10).plot(kind="bar")
plt.title("Top Job Locations")
plt.savefig("results/top_locations.png")
plt.close()

# ===============================
# ---------- FEATURE ENGINEERING ----------
# ===============================

# Skill count (USED BY MODEL)
df["skill_count"] = df["required_skills"].apply(
    lambda x: len(str(x).split(",")) if x != "Unknown" else 0
)

# ⚠️ Certificate count is NOT used by model
# Keep it only for analysis (optional)
if "certificates" in df.columns:
    df["certificate_count"] = df["certificates"].apply(
        lambda x: len(str(x).split(",")) if x != "Unknown" else 0
    )

# ===============================
# ---------- SAVE CLEAN DATA ----------
# ===============================
df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ Feature-engineered dataset saved to:")
print(OUTPUT_PATH)
print("🎯 Feature engineering completed successfully")
