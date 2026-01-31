import sqlite3
import os
import pandas as pd

# ===============================
# PATH SETUP
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "jobai.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def show_db_summary():
    conn = get_db_connection()

    print("\n📊 DATABASE ANALYTICS SUMMARY")
    print("=" * 45)

    # -------------------------------
    # Total Predictions
    # -------------------------------
    total = pd.read_sql(
        "SELECT COUNT(*) AS total FROM predictions",
        conn
    )
    print(f"\nTotal Predictions: {total.iloc[0]['total']}")

    # -------------------------------
    # Demand Distribution
    # -------------------------------
    dist = pd.read_sql("""
        SELECT demand, COUNT(*) as count
        FROM predictions
        GROUP BY demand
    """, conn)

    print("\nDemand Distribution:")
    print(dist)

    # -------------------------------
    # Last 10 Predictions
    # -------------------------------
    recent = pd.read_sql("""
        SELECT jobtitle, location, demand, confidence, created_at
        FROM predictions
        ORDER BY created_at DESC
        LIMIT 10
    """, conn)

    print("\nLast 10 Predictions:")
    print(recent)

    conn.close()

if __name__ == "__main__":
    show_db_summary()
