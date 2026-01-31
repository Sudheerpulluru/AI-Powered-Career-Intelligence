import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

print("📂 Looking inside:", DATA_DIR)
print("📄 Files found:", os.listdir(DATA_DIR))

# 🔍 Find CSV file automatically
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

if not csv_files:
    raise FileNotFoundError("❌ No CSV file found in data/processed")

CSV_PATH = os.path.join(DATA_DIR, csv_files[0])
DB_PATH = os.path.join(BASE_DIR, "jobai.db")

print("✅ Using CSV:", CSV_PATH)
print("💾 Using DB :", DB_PATH)

# Load CSV
df = pd.read_csv(CSV_PATH)
print("✅ CSV loaded successfully")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

# Save to SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql(
    "job_market_data",
    conn,
    if_exists="replace",
    index=False
)
conn.close()

print("🎉 CSV → SQLite migration completed")
print("📊 Table created: job_market_data")
