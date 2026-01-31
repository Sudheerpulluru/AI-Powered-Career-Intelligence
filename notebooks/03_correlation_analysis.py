import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===============================
# LOAD CLEAN DATA
# ===============================
df = pd.read_csv("data/processed/job_market_clean.csv")

# ===============================
# FEATURE ENGINEERING (LOCAL)
# ===============================
# Recreate skill_count safely
df["required_skills"] = df["required_skills"].fillna("")
df["skill_count"] = df["required_skills"].apply(
    lambda x: len(str(x).split(","))
)

# Encode demand label numerically
demand_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}
df["demand_numeric"] = df["demand_label"].map(demand_map)

# ===============================
# SELECT NUMERIC FEATURES
# ===============================
corr_features = df[[
    "skill_count",
    "demand_numeric"
]]

# ===============================
# CORRELATION MATRIX
# ===============================
correlation_matrix = corr_features.corr()

# Create output folder
os.makedirs("results/plots", exist_ok=True)

# ===============================
# HEATMAP
# ===============================
plt.figure(figsize=(5, 4))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5
)
plt.title("Correlation Between Skill Count and Job Demand")
plt.tight_layout()
plt.savefig("results/plots/correlation_heatmap.png")
plt.close()

print("✅ Correlation analysis completed successfully")
