import sqlite3

conn = sqlite3.connect("jobai.db")
cursor = conn.cursor()

# ===============================
# 🔥 CLEAR OLD PREDICTIONS (TEMPORARY)
# ===============================
cursor.execute("DELETE FROM predictions")
conn.commit()
print("✅ Old predictions cleared")

# ===============================
# 1. Show tables
# ===============================
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\n📌 Tables in database:")
print(tables)

# ===============================
# 2. Show recent predictions
# ===============================
try:
    cursor.execute("""
        SELECT * FROM predictions
        ORDER BY id DESC
        LIMIT 5;
    """)
    rows = cursor.fetchall()
    print("\n📊 Recent Predictions:")
    for row in rows:
        print(row)
except Exception:
    print("\n⚠️ Predictions table not found or empty.")

conn.close()
