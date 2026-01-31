"""
MAIN EXECUTION FILE – REVIEW 2
Runs:
1. Baseline models
2. Advanced model + hyperparameter tuning
3. Statistical validation
4. Business optimization
5. Interactive prediction demo (INPUT → OUTPUT)

Command:
python main.py
"""

import os
import sys
import subprocess

# ===============================
# FORCE SAFE NON-GUI MODE
# ===============================
os.environ["MPLBACKEND"] = "Agg"
os.environ["SHOW_PLOTS"] = "0"

# ===============================
# PROJECT ROOT
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_step(title, script_path):
    print("\n" + "=" * 70)
    print(f"▶ {title}")
    print("=" * 70)
    subprocess.run([sys.executable, script_path], check=True)

print("\n🚀 JOB MARKET ANALYTICS – REVIEW 2")
print("=" * 70)

# ===============================
# STEP 1: BASELINE MODELS
# ===============================
run_step(
    "Review-2 Point 2: Baseline Model Comparison",
    os.path.join(PROJECT_ROOT, "src", "models", "baseline_models.py")
)

# ===============================
# STEP 2: ADVANCED MODEL + HYPERPARAMETER TUNING
# ===============================
run_step(
    "Review-2 Point 3 & 4: Advanced Model + Hyperparameter Tuning",
    os.path.join(PROJECT_ROOT, "src", "models", "train_demand_model.py")
)

# ===============================
# STEP 3: STATISTICAL VALIDATION
# ===============================
run_step(
    "Review-2 Point 6: Statistical Validation",
    os.path.join(PROJECT_ROOT, "src", "models", "statistical_validation.py")
)

# ===============================
# STEP 4: BUSINESS OPTIMIZATION
# ===============================
run_step(
    "Review-2 Point 7: Business Optimization",
    os.path.join(PROJECT_ROOT, "src", "models", "business_optimization.py")
)

# ===============================
# STEP 5: LIVE INPUT → OUTPUT DEMO
# ===============================
print("\n" + "=" * 70)
print("▶ Review-2 Point 5: Model Interpretation (INPUT → OUTPUT)")
print("=" * 70)

MODELS_PATH = os.path.join(PROJECT_ROOT, "src", "models")
if MODELS_PATH not in sys.path:
    sys.path.insert(0, MODELS_PATH)

import demand_predictor

# -------------------------------
# SAMPLE DEMO
# -------------------------------
print("\n🧾 Sample Input Example:")
print("Job Title: AI Engineer")
print("Location: India")
print("Experience: 2-5 years")
print("Industry: Software")
print("Skills: Python, Machine Learning, AWS\n")

demand, confidence, career_risk, ai_probability = demand_predictor.predict_job_demand(
    "AI Engineer",
    "India",
    "2-5 years",
    "Software",
    "Python, Machine Learning, AWS"
)

print("📤 Output:")
print(f"Predicted Demand   : {demand}")
print(f"Confidence Score   : {confidence}%")
print(f"Career Risk Level  : {career_risk}")
print(f"AI Exposure Chance : {ai_probability}%")

# -------------------------------
# INTERACTIVE MODE
# -------------------------------
print("\n🔁 INTERACTIVE MODE (type 'exit' to stop)")

while True:
    jobtitle = input("\nJob Title: ")
    if jobtitle.lower() == "exit":
        break

    location = input("Location: ")
    experience = input("Experience Level: ")
    industry = input("Industry: ")
    skills = input("Skills (comma separated): ")

    demand, confidence, career_risk, ai_probability = demand_predictor.predict_job_demand(
        jobtitle, location, experience, industry, skills
    )

    print("\n📊 Prediction Result")
    print("---------------------")
    print(f"Predicted Demand   : {demand}")
    print(f"Confidence Score   : {confidence}%")
    print(f"Career Risk Level  : {career_risk}")
    print(f"AI Exposure Chance : {ai_probability}%")

print("\n🎉 ALL REVIEW-2 TASKS COMPLETED SUCCESSFULLY")
print("✅ READY FOR MENTOR DEMO")
print("=" * 70)
