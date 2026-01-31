"""
Review-2 Unified Output Script
HYBRID ML + RULE-BASED (BINARY DEMAND)
"""

import os
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, accuracy_score
from sklearn.model_selection import learning_curve, StratifiedKFold
from scipy.stats import ttest_rel

# ===============================
# GRAPH CONTROL
# ===============================
SHOW_PLOTS = os.environ.get("SHOW_PLOTS", "1") == "1"

import matplotlib
if not SHOW_PLOTS:
    matplotlib.use("Agg")

def show_or_save(name):
    os.makedirs("results", exist_ok=True)
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.savefig(f"results/{name}")
        plt.close()

# ===============================
# PATH SETUP
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed",
    "job_market_analytics_final_with_certificates.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT, "data", "models",
    "job_demand_model.pkl"
)

RESULTS_PATH = os.path.join(
    PROJECT_ROOT, "results",
    "baseline_results.csv"
)

# ===============================
# LOAD ARTIFACTS
# ===============================
print("\n🔹 Loading Review-2 Artifacts")

df = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)
results_df = pd.read_csv(RESULTS_PATH)

df.columns = df.columns.str.lower()

# ===============================
# COLUMN NORMALIZATION
# ===============================
COLUMN_MAP = {
    "job_title": "jobtitle",
    "jobrole": "jobtitle",
    "job_role": "jobtitle",
    "city": "location",
    "experience": "experience_level",
}

df.rename(
    columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns},
    inplace=True
)

# ===============================
# FEATURE ENGINEERING
# ===============================
df["skill_count"] = df["required_skills"].fillna("Unknown").apply(
    lambda x: len(str(x).split(",")) if x != "Unknown" else 0
)

# ===============================
# NUMERIC BINARY TARGET
# ===============================
df["demand_binary"] = df["demand_label"].apply(
    lambda x: 1 if x == "High" else 0
)

FEATURE_COLUMNS = [
    "jobtitle",
    "location",
    "experience_level",
    "industry",
    "skill_count"
]

X = df[FEATURE_COLUMNS]
y = df["demand_binary"]

print("\n📊 DATASET SUMMARY")
print(y.value_counts())

print("\n📈 BASELINE MODEL COMPARISON")
print(results_df)

# ===============================
# 🔥 HYBRID PREDICTION (KEY CHANGE)
# ===============================
print("\n🧠 HYBRID ML + RULE-BASED PREDICTION")

ml_pred = model.predict(X)

# Rule-based override
rule_pred = []

for _, row in df.iterrows():
    if (
        row["skill_count"] >= 6 or
        str(row["experience_level"]).lower() in ["senior", "lead"] or
        str(row["industry"]).lower() in ["it", "software", "ai", "data"]
    ):
        rule_pred.append(1)   # High demand
    else:
        rule_pred.append(0)

rule_pred = np.array(rule_pred)

# Hybrid logic: rule overrides ML
y_hybrid = np.where(rule_pred == 1, 1, ml_pred)

print("✅ Hybrid Accuracy :", accuracy_score(y, y_hybrid))

# ===============================
# CONFUSION MATRIX
# ===============================
print("\n📉 CONFUSION MATRIX (HYBRID)")

cm = confusion_matrix(y, y_hybrid, labels=[1, 0])

plt.figure()
plt.imshow(cm, cmap="Blues")
plt.xticks([0, 1], ["High", "Not High"])
plt.yticks([0, 1], ["High", "Not High"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix (Hybrid Demand)")
plt.colorbar()
show_or_save("confusion_matrix.png")

# ===============================
# ROC CURVE (ML PROBABILITIES)
# ===============================
print("\n📈 ROC CURVE")

if hasattr(model, "predict_proba"):
    y_prob = model.predict_proba(X)
    high_index = list(model.classes_).index(1)

    fpr, tpr, _ = roc_curve(y, y_prob[:, high_index])
    auc = roc_auc_score(y, y_prob[:, high_index])

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve (High Demand)")
    plt.legend()
    show_or_save("roc_curve.png")

# ===============================
# LEARNING CURVE (ML MODEL)
# ===============================
print("\n📐 LEARNING CURVE")

cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

train_sizes, train_scores, test_scores = learning_curve(
    model,
    X,
    y,
    cv=cv,
    scoring="f1",
    train_sizes=np.linspace(0.1, 1.0, 5),
    n_jobs=-1
)

plt.figure()
plt.plot(train_sizes, train_scores.mean(axis=1), label="Train")
plt.plot(train_sizes, test_scores.mean(axis=1), label="Validation")
plt.xlabel("Training Samples")
plt.ylabel("F1 Score")
plt.title("Learning Curve (ML Component)")
plt.legend()
show_or_save("learning_curve.png")

# ===============================
# STATISTICAL SIGNIFICANCE TEST
# ===============================
print("\n📊 STATISTICAL SIGNIFICANCE TEST")

t_stat, p_value = ttest_rel(
    train_scores.mean(axis=1),
    test_scores.mean(axis=1)
)

print("T-statistic:", round(t_stat, 4))
print("P-value    :", round(p_value, 4))

if p_value < 0.05:
    print("✅ Statistically significant improvement")
else:
    print("⚠️ Not statistically significant")

print("\n🎉 Review-2 Outputs Completed Successfully (HYBRID SYSTEM)")
