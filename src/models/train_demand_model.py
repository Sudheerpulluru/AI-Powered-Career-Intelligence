import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_class_weight

print("🔹 Training script started (BINARY DEMAND MODE)")

# ===============================
# PATH SETUP
# ===============================
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed",
    "job_market_analytics_final_with_certificates.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT, "data", "models", "job_demand_model.pkl"
)

REPORT_PATH = os.path.join(PROJECT_ROOT, "results", "reports")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.lower()
df = df.replace([np.inf, -np.inf], np.nan)
df.fillna("Unknown", inplace=True)

# ===============================
# COLUMN NORMALIZATION
# ===============================
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

REQUIRED_COLUMNS = [
    "jobtitle",
    "location",
    "experience_level",
    "industry",
    "required_skills",
    "demand_label"
]

df = df[REQUIRED_COLUMNS]

# ===============================
# FEATURE ENGINEERING
# ===============================
df["skill_count"] = df["required_skills"].apply(
    lambda x: len(str(x).split(",")) if x != "Unknown" else 0
)

df.drop(columns=["required_skills"], inplace=True)

# ===============================
# 🔥 BINARY TARGET (NUMERIC – CRITICAL FIX)
# ===============================
# High → 1, Not High → 0
df["demand_binary"] = df["demand_label"].apply(
    lambda x: 1 if x == "High" else 0
)

X = df.drop(["demand_label", "demand_binary"], axis=1)
y = df["demand_binary"]

# ===============================
# TRAIN / TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ===============================
# PREPROCESSING PIPELINE
# ===============================
categorical_cols = [
    "jobtitle", "location", "experience_level", "industry"
]
numeric_cols = ["skill_count"]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_cols
        ),
        ("num", "passthrough", numeric_cols)
    ]
)

# ===============================
# CLASS WEIGHTS (NOW NUMERIC)
# ===============================
classes = np.unique(y_train)

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weight_dict = dict(zip(classes, class_weights))
print("\n⚖️ Class Weights:", class_weight_dict)

# ===============================
# MODEL
# ===============================
rf = RandomForestClassifier(
    class_weight=class_weight_dict,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", rf)
    ]
)

# ===============================
# HYPERPARAMETER TUNING (FIXED)
# ===============================
param_dist = {
    "model__n_estimators": [300, 400, 500],
    "model__max_depth": [15, 20, 25],
    "model__min_samples_split": [2, 5],
    "model__min_samples_leaf": [1, 2]
}

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_dist,
    n_iter=10,
    cv=3,
    scoring="f1",          # works correctly now (numeric labels)
    random_state=42,
    n_jobs=-1,
    error_score="raise"
)

print("\n🔍 Starting hyperparameter tuning...")
search.fit(X_train, y_train)

pipeline = search.best_estimator_

# ===============================
# SAVE BEST PARAMETERS
# ===============================
os.makedirs(REPORT_PATH, exist_ok=True)
with open(os.path.join(REPORT_PATH, "best_params.txt"), "w") as f:
    f.write(str(search.best_params_))

print("\n✅ Best Parameters Saved")

# ===============================
# EVALUATION
# ===============================
y_pred = pipeline.predict(X_test)

print("\n📈 Model Performance (BINARY):")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, pos_label=1))
print("Recall   :", recall_score(y_test, y_pred, pos_label=1))
print("F1 Score :", f1_score(y_test, y_pred, pos_label=1))

# ===============================
# SAVE MODEL
# ===============================
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)

print("\n💾 Model saved successfully")
print("🏁 Training completed successfully")
