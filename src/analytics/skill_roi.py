# src/analytics/skill_roi.py

"""
Skill ROI Analytics
-------------------
Evaluates return on investment of learning a skill based on
salary growth, risk reduction, and learning time.

Also provides normalized ROI score for AI impact analysis.
"""


def calculate_skill_roi(
    skill,
    current_salary,
    future_salary,
    learning_months,
    current_risk,
    future_risk
):
    """
    Skill ROI Engine
    Returns ROI score and recommendation
    """

    # Salary boost percentage
    salary_boost = ((future_salary - current_salary) / current_salary) * 100

    # Risk reduction
    risk_reduction = current_risk - future_risk

    # Normalize values (0–10 scale)
    salary_score = min(salary_boost / 10, 10)
    risk_score = min(risk_reduction / 10, 10)
    time_penalty = min(learning_months, 12) / 12 * 10

    # ROI formula
    roi_score = (
        salary_score * 0.4 +
        risk_score * 0.4 -
        time_penalty * 0.2
    )
    roi_score = round(max(0, roi_score), 2)

    # Recommendation
    if roi_score >= 7:
        decision = "Highly Recommended"
    elif roi_score >= 4:
        decision = "Worth Learning"
    else:
        decision = "Low Priority"

    return {
        "skill": skill,
        "roi_score": roi_score,
        "salary_boost_percent": round(salary_boost, 1),
        "risk_reduction": round(risk_reduction, 1),
        "learning_months": learning_months,
        "decision": decision
    }


# ✅ NEW: Normalized Skill Safety Score (0–1)
# Used for AI Takeover Probability
def normalized_skill_safety(roi_score):
    """
    Converts ROI score (0–10) to safety score (0–1)
    Higher = more resistant to AI automation
    """
    return round(min(roi_score / 10, 1.0), 2)
