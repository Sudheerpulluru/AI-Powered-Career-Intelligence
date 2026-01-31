import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load feature engineered data
df = pd.read_csv("data/featured_jobs.csv")
print("Dataset shape:", df.shape)

# ----- TARGET CREATION (Demand Level) -----
def demand_label(row):
    score = 0

    if row["skill_count"] >= 5:
        score += 1
    if row["location_tier"] == "Metro":
        score += 1

    if score >= 2:
        return "High"
    elif score == 1:
        return "Medium"
    else:
        return "Low"

df["demand_level"] = df.apply(demand_label, axis=1)

# ----- FEATURE SELECTION -----
features = ["skill_count", "location_tier"]

X = df[features]
y = df["demand_level"]

# Encode categorical features
le_location = LabelEncoder()
X["location_tier"] = le_location.fit_transform(X["location_tier"])

le_target = LabelEncoder()
y = le_target.fit_transform(y)

# ----- TRAIN TEST SPLIT -----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----- MODEL TRAINING -----
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ----- EVALUATION -----
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# ----- SAVE MODEL -----
joblib.dump(model, "data/job_demand_model.pkl")
joblib.dump(le_target, "data/label_encoder.pkl")

print("Model training completed and saved")
