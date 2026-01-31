import pandas as pd
import numpy as np
import os

def calculate_job_volatility(history_file):
    """
    Job Volatility Index (JVI) and Job Stability Score (JSS)

    JVI  = Standard deviation of job demand frequency
    JSS  = Inverse of volatility (higher = more stable)
    """

    if not os.path.exists(history_file):
        return {
            "volatility_index": 0,
            "stability_score": 1.0,
            "risk_level": "Unknown"
        }

    df = pd.read_csv(history_file)

    if df.empty or "prediction" not in df.columns:
        return {
            "volatility_index": 0,
            "stability_score": 1.0,
            "risk_level": "Unknown"
        }

    # Convert demand labels to numeric scores
    demand_map = {"Low": 1, "Medium": 2, "High": 3}
    df["demand_score"] = df["prediction"].map(demand_map)

    # Volatility = standard deviation
    volatility = round(df["demand_score"].std(), 2)

    # Stability score (inverse relationship)
    stability = round(1 / (volatility + 1), 2)

    # Risk classification
    if volatility >= 0.8:
        risk = "High Risk"
    elif volatility >= 0.4:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return {
        "volatility_index": volatility,
        "stability_score": stability,
        "risk_level": risk
    }
