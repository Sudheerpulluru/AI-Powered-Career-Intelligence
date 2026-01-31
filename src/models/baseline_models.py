import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

print("\n📊 BASELINE MODEL COMPARISON (WITH AUC)\n")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("data/processed/job_market_analytics_final_with_certificates.csv")
df.fillna("Unknown", inplace=True)
df.columns = [c.lower() for c in df.columns]

# 🔑 COLUMN NORMALIZATION (CRITICAL FIX)
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
# FEATURE ENGINEERING
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
# TRAIN TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

categorical_cols = ["jobtitle", "location", "experience_level", "industry"]
numeric_cols = ["skill_count"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numeric_cols)
])

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42)
}

for name, model in models.items():
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    # AUC requires probabilities
    if hasattr(model, "predict_proba"):
        y_prob = pipe.predict_proba(X_test)
        auc = roc_auc_score(pd.get_dummies(y_test), y_prob, multi_class="ovr")
    else:
        auc = "N/A"

    print(f"\n🔹 {name}")
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, average="weighted"))
    print("Recall   :", recall_score(y_test, y_pred, average="weighted"))
    print("F1 Score :", f1_score(y_test, y_pred, average="weighted"))
    print("AUC      :", auc)
