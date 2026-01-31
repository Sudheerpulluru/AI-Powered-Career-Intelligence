print("\n===== REVIEW 3 OUTPUT (FLASK PROJECT) =====\n")

import sqlite3
import pandas as pd
import joblib

# 1. DB Connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
print("✅ Database Connected")

# 2. Show Tables
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';", conn
)
print("\n📌 Tables:")
print(tables)

# 3. Ensure customers table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    experience INTEGER,
    salary INTEGER
)
""")
conn.commit()
print("\n✅ customers table verified")

# 4. Insert sample data if table is empty
count = cursor.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

if count == 0:
    cursor.execute("""
    INSERT INTO customers (age, experience, salary)
    VALUES
    (22, 1, 30000),
    (25, 3, 45000),
    (30, 6, 70000)
    """)
    conn.commit()
    print("✅ Sample data inserted into customers table")

# 5. Fetch Data from DB
df = pd.read_sql("SELECT * FROM customers LIMIT 5;", conn)
print("\n📊 Sample Data from DB:")
print(df)

# 6. Load Model
model = joblib.load("model.pkl")
print("\n🤖 Model Loaded")

# 7. Prediction
X = df.drop(columns=["id"], errors="ignore")
predictions = model.predict(X)
df["prediction"] = predictions

print("\n📈 Predictions:")
print(df[["prediction"]])

# 8. Save Predictions
df.to_sql("predictions", conn, if_exists="append", index=False)
print("\n💾 Predictions Saved to DB")

conn.close()
print("\n===== REVIEW 3 COMPLETED SUCCESSFULLY =====\n")
# 🔍 View DB contents
conn = sqlite3.connect("database.db")

print("\n📌 Tables in Database:")
print(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn))

print("\n📊 Customers Table:")
print(pd.read_sql("SELECT * FROM customers;", conn))

print("\n📈 Predictions Table:")
print(pd.read_sql("SELECT * FROM predictions;", conn))

conn.close()
