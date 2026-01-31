import sqlite3
import pandas as pd
import os

# ===============================
# PATH SETUP
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, "jobai.db")

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "job_market_analytics_final_with_certificates.csv"
)

print("🔹 Starting CSV → Database Migration")

# ===============================
# LOAD CSV
# ===============================
df = pd.read_csv(CSV_PATH)
df.fillna("Unknown", inplace=True)
df.columns = [c.lower() for c in df.columns]

print(f"📄 CSV Loaded: {df.shape[0]} rows")

# ===============================
# CONNECT TO DATABASE
# ===============================
conn = sqlite3.connect(DB_PATH)

# ===============================
# WRITE TO DATABASE
# ===============================
df.to_sql(
    "jobs",
    conn,
    if_exists="replace",   # Safe for demo
    index=False
)

print("✅ Data successfully migrated to 'jobs' table")

# ===============================
# VERIFY INSERTION
# ===============================
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM jobs")
count = cursor.fetchone()[0]

print(f"📊 Rows in jobs table: {count}")

conn.close()
print("🏁 Migration completed successfully")
