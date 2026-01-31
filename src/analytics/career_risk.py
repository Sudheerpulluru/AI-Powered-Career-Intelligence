# src/analytics/career_risk.py

"""
Career Risk Analytics Module
----------------------------
This module calculates career risk using
- Job demand
- Market volatility
- Skill obsolescence

Designed as an explainable analytics model
(not a black-box ML prediction).
"""


def calculate_career_risk(demand, volatility_index, role):
    """
    Career Risk Radar
    Returns risk score (0–100) and category
    """

    # 1️⃣ Demand Risk
    demand_risk_map = {
        "High": 20,
        "Medium": 50,
        "Low": 80
    }
    demand_risk = demand_risk_map.get(demand, 50)

    # 2️⃣ Volatility Risk (scaled)
    # volatility_index expected range: 0–1
    volatility_risk = min(volatility_index * 100, 100)

    # 3️⃣ Skill Obsolescence Risk (domain-based)
    fast_changing_roles = [
        "AI Engineer",
        "Data Scientist",
        "ML Engineer",
        "Blockchain Consultant",
        "Cloud Engineer"
    ]

    if role in fast_changing_roles:
        skill_risk = 70
    else:
        skill_risk = 40

    # 🔢 Final weighted risk score
    risk_score = (
        demand_risk * 0.3 +
        volatility_risk * 0.4 +
        skill_risk * 0.3
    )

    risk_score = round(risk_score, 1)

    # Risk category
    if risk_score >= 70:
        category = "High Risk"
    elif risk_score >= 40:
        category = "Medium Risk"
    else:
        category = "Low Risk"

    return {
        "risk_score": risk_score,
        "risk_category": category,
        "breakdown": {
            "demand_risk": demand_risk,
            "volatility_risk": round(volatility_risk, 1),
            "skill_risk": skill_risk
        }
    }


# ✅ NEW: Normalized Job Risk (0–1 scale)
# This is useful for AI Takeover & dashboard analytics
def calculate_overall_job_risk(volatility, trend_score, shock_impact):
    """
    volatility: 0–1 (market instability)
    trend_score: 0–1 (job demand growth)
    shock_impact: 0–1 (automation / layoffs)
    """
    risk = (
        volatility * 0.4 +
        (1 - trend_score) * 0.4 +
        shock_impact * 0.2
    )
    return round(risk, 2)


def risk_label(score):
    """
    Converts normalized risk score to label
    """
    if score < 0.3:
        return "Low"
    elif score < 0.6:
        return "Medium"
    return "High"
