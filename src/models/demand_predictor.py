import numpy as np

# ===============================
# ROLE BASE DEMAND (EXPLAINABLE)
# ===============================
ROLE_BASE_DEMAND = {
    "data analyst": 60,
    "software engineer": 65,
    "data engineer": 70,
    "ai engineer": 75
}

# ===============================
# AI EXPOSURE (ROLE-BASED)
# ===============================
AI_EXPOSURE_BASE = {
    "data analyst": 65,
    "software engineer": 45,
    "data engineer": 40,
    "ai engineer": 30
}

# ===============================
# EXPERIENCE BONUS
# ===============================
def experience_bonus(exp):
    exp = exp.lower()
    if exp == "fresher":
        return -10
    elif exp == "2-5 years":
        return 5
    elif exp == "5+ years":
        return 10
    return 0

# ===============================
# SKILL BONUS
# ===============================
def skill_bonus(skill_count):
    if skill_count >= 5:
        return 15
    elif skill_count >= 3:
        return 5
    else:
        return -10

# ===============================
# MAIN PREDICTOR
# ===============================
def predict_job_demand(jobtitle, location, experience_level, industry, required_skills):

    role = jobtitle.lower().strip()
    skills = [s.strip() for s in required_skills.split(",") if s.strip()]
    skill_count = len(skills)

    # Base score
    base = ROLE_BASE_DEMAND.get(role, 55)

    demand_score = (
        base
        + experience_bonus(experience_level)
        + skill_bonus(skill_count)
    )

    demand_score = max(0, min(100, demand_score))

    # -----------------------------
    # DEMAND LABEL
    # -----------------------------
    if demand_score >= 75:
        demand = "High"
    elif demand_score >= 50:
        demand = "Medium"
    else:
        demand = "Low"

    # -----------------------------
    # CONFIDENCE (DEMO SAFE)
    # -----------------------------
    confidence = round(min(max(demand_score, 40), 85), 2)

    # -----------------------------
    # CAREER RISK
    # -----------------------------
    if demand == "High":
        career_risk = "Low Risk"
    elif demand == "Medium":
        career_risk = "Medium Risk"
    else:
        career_risk = "High Risk"

    # -----------------------------
    # AI EXPOSURE
    # -----------------------------
    base_ai = AI_EXPOSURE_BASE.get(role, 55)

    if skill_count <= 2:
        ai_probability = base_ai + 10
    elif skill_count >= 5:
        ai_probability = base_ai - 5
    else:
        ai_probability = base_ai

    ai_probability = max(10, min(90, ai_probability))

    return demand, confidence, career_risk, ai_probability
