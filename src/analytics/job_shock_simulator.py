# src/analytics/job_shock_simulator.py

"""
Job Shock Simulator
-------------------
Simulates external shocks such as recession, AI automation,
and mass layoffs to evaluate career resilience.

This module is used for:
- Job Risk analysis
- AI automation exposure
- Scenario-based decision support
"""


def simulate_job_shock(role, base_demand, base_salary, base_risk):
    """
    Simulates impact of external shocks on a career

    base_demand: numeric index (e.g., demand score)
    base_salary: monthly or annual salary
    base_risk: current career risk (0–100)
    """

    shocks = {
        "Recession": {
            "demand_factor": 0.7,
            "salary_factor": 0.85,
            "risk_increase": 20,
            "automation_shock": 0.1
        },
        "AI Automation": {
            "demand_factor": 0.6 if role in ["QA Engineer", "Data Analyst"] else 0.9,
            "salary_factor": 0.8,
            "risk_increase": 25,
            "automation_shock": 0.6
        },
        "Mass Layoffs": {
            "demand_factor": 0.75,
            "salary_factor": 0.9,
            "risk_increase": 15,
            "automation_shock": 0.3
        }
    }

    results = {}

    for shock, impact in shocks.items():
        new_demand = base_demand * impact["demand_factor"]
        new_salary = base_salary * impact["salary_factor"]
        new_risk = min(base_risk + impact["risk_increase"], 100)

        resilience_score = max(0, 100 - new_risk)

        results[shock] = {
            "demand_change_percent": round((new_demand - base_demand) / base_demand * 100, 1),
            "salary_change_percent": round((new_salary - base_salary) / base_salary * 100, 1),
            "risk_change": impact["risk_increase"],
            "resilience_score": resilience_score,
            "automation_shock": impact["automation_shock"]
        }

    return results


# ✅ NEW: Extract AI automation impact (used in AI Takeover analysis)
def extract_automation_shock(shock_results):
    """
    Returns normalized automation shock (0–1)
    """
    ai_shock = shock_results.get("AI Automation", {}).get("automation_shock", 0.3)
    return round(ai_shock, 2)
