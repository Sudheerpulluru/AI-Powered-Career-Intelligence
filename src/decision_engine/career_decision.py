def career_decision(current_role, target_role, current_metrics, target_metrics):
    """
    Career Decision Engine
    Combines salary, demand, and market risk
    """

    decision_score = 0
    reasons = []

    # 1️⃣ Salary comparison
    if target_metrics["salary_max"] > current_metrics["salary_max"]:
        decision_score += 2
        reasons.append("Target role offers higher salary potential")

    # 2️⃣ Demand comparison
    if target_metrics["demand"] == "High":
        decision_score += 2
        reasons.append("Target role has strong market demand")

    # 3️⃣ Stability comparison
    if target_metrics["risk_level"] == "Low Risk":
        decision_score += 2
        reasons.append("Target role is more market-stable")

    # 4️⃣ Skill readiness (soft weight)
    if target_metrics.get("skill_match", 0) >= 60:
        decision_score += 1
        reasons.append("Your skills are reasonably aligned")

    # Final verdict
    if decision_score >= 5:
        verdict = "✅ Safe to Switch"
    elif decision_score >= 3:
        verdict = "⚠ Switch with Preparation"
    else:
        verdict = "❌ Not Recommended Now"

    return {
        "verdict": verdict,
        "score": decision_score,
        "reasons": reasons
    }
