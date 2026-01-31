import pandas as pd
import numpy as np
import joblib
from scipy.stats import ttest_rel

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

print("🔍 Statistical Validation Started")

# ===============================
# LOAD TRAINED PIPELINE (ONLY FOR PREPROCESSOR)
# ===============================
trained_pipeline = joblib.load("data/models/job_demand_model.pkl")
preprocessor = trained_pipeline.named_steps["preprocessor"]

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("data/processed/job_market_analytics_final_with_certificates.csv")
df.fillna("Unknown", inplace=True)
df.columns = [c.lower() for c in df.columns]

# 🔑 SAME COLUMN NORMALIZATION AS TRAINING
COLUMN_MAP = {
    "job_title": "jobtitle",
    "jobrole": "jobtitle",
    "job_role": "jobtitle",
    "city": "location",
    "experience": "experience_level",
    "skills": "required_skills"
}

df.rename(
    columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns},
    inplace=True
)

# ===============================
# SAME FEATURE ENGINEERING
# ===============================
df["skill_count"] = df["required_skills"].apply(
    lambda x: len(str(x).split(",")) if x != "Unknown" else 0
)
df.drop(columns=["required_skills"], inplace=True)

REQUIRED_COLUMNS = [
    "jobtitle",
    "location",
    "experience_level",
    "industry",
    "skill_count",
    "demand_label"
]

df = df[REQUIRED_COLUMNS]

X = df.drop("demand_label", axis=1)
y = df["demand_label"]

# ===============================
# BASELINE MODEL (NO CLASS WEIGHT)
# ===============================
baseline_rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

baseline_pipe = Pipeline([
    ("preprocessor", preprocessor),
    ("model", baseline_rf)
])

# ===============================
# TUNED MODEL (NO CLASS WEIGHT – FOR FAIR VALIDATION)
# ===============================
tuned_rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

tuned_pipe = Pipeline([
    ("preprocessor", preprocessor),
    ("model", tuned_rf)
])

# ===============================
# CROSS-VALIDATION
# ===============================
baseline_scores = cross_val_score(
    baseline_pipe,
    X, y,
    cv=3,
    scoring="f1_weighted"
)

tuned_scores = cross_val_score(
    tuned_pipe,
    X, y,
    cv=3,
    scoring="f1_weighted"
)

print("\nBaseline CV Scores:", baseline_scores)
print("Tuned CV Scores   :", tuned_scores)

# ===============================
# PAIRED T-TEST
# ===============================
t_stat, p_value = ttest_rel(tuned_scores, baseline_scores)

print("\n📊 Paired T-Test Results")
print("t-statistic:", t_stat)
print("p-value    :", p_value)

if p_value < 0.05:
    print("✅ Improvement is statistically significant")
else:
    print("⚠️ Improvement is NOT statistically significant")
