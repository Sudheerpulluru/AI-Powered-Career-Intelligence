import pandas as pd
import os

# ===============================
# PATH CONFIGURATION
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(
    BASE_DIR, "data", "raw", "indian_jobs.csv"
)

CLEAN_DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "job_market_clean.csv"
)


# ===============================
# CLEANING PIPELINE
# ===============================
def clean_job_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning pipeline for Job Market Analytics project.
    Handles missing values, duplicates, and text normalization.
    """

    # Remove duplicate records
    df = df.drop_duplicates()

    # Handle missing values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("Unknown")
        else:
            df[col] = df[col].fillna(df[col].median())

    # Normalize text columns
    text_cols = ["skills", "joblocation_address"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    return df


# ===============================
# FEATURE ENGINEERING
# ===============================
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature engineering for job market analysis.
    """

    # Skill count feature
    df["skill_count"] = df["skills"].apply(
        lambda x: len(x.split(",")) if x != "unknown" else 0
    )

    # Location tier feature
    metros = ["bangalore", "hyderabad", "pune", "chennai", "mumbai", "delhi"]

    df["location_tier"] = df["joblocation_address"].apply(
        lambda x: "Metro" if any(city in x for city in metros) else "Non-Metro"
    )

    return df


# ===============================
# PIPELINE EXECUTION
# ===============================
if __name__ == "__main__":
    df = pd.read_csv(RAW_DATA_PATH)
    print("Raw dataset loaded:", df.shape)

    df = clean_job_data(df)
    print("Data cleaning completed")

    df = feature_engineering(df)
    print("Feature engineering completed")

    df.to_csv(CLEAN_DATA_PATH, index=False)
    print("Clean dataset saved to:", CLEAN_DATA_PATH)
