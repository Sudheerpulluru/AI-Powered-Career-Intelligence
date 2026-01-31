from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from functools import wraps
from datetime import timedelta
import csv
import os
import sqlite3

# ===============================
# 🔥 ML + RULE BASED LOGIC
# ===============================
from src.models.demand_predictor import predict_job_demand

print("🔥 RUNNING app.py FILE")

# ===============================
# APP SETUP
# ===============================
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "jobai_secret_key"
app.permanent_session_lifetime = timedelta(days=7)

# ===============================
# PATHS
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "jobai.db")
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# ===============================
# INIT USERS FILE
# ===============================
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["email", "password"])

# ===============================
# DATABASE HELPERS
# ===============================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_predictions_table():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jobtitle TEXT,
                location TEXT,
                experience_level TEXT,
                industry TEXT,
                skill_count INTEGER,
                demand TEXT,
                confidence REAL,
                created_at TEXT
            )
        """)


def save_prediction_to_db(data):
    ensure_predictions_table()
    with get_db_connection() as conn:
        conn.execute("""
            INSERT INTO predictions
            (jobtitle, location, experience_level,
             industry, skill_count, demand, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            data["jobtitle"],
            data["location"],
            data["experience_level"],
            data["industry"],
            data["skill_count"],
            data["demand"],
            data["confidence"]
        ))


def get_last_10_predictions():
    ensure_predictions_table()
    with get_db_connection() as conn:
        rows = conn.execute("""
            SELECT jobtitle, location, experience_level,
                   industry, skill_count, demand,
                   confidence, created_at
            FROM predictions
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()
    return [dict(row) for row in rows]


ensure_predictions_table()
print("✅ predictions table ready")

# ===============================
# DECORATORS
# ===============================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def prediction_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("prediction_done"):
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return wrapper

# ===============================
# SESSION INITIALIZATION
# ===============================
def init_prediction_state():
    session.clear()
    session.update({
        "prediction_done": False,
        "user_input": {},
        "demand": None,
        "career_risk": None,
        "ai_probability": None,
        "career_decision": None,
        "confidence": None,
        "demand_trend": [40, 42, 44, 46, 48, 50],
        "volatility_trend": [30, 28, 35, 32, 38, 34]
    })

# ===============================
# AUTH ROUTES
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with open(USERS_FILE) as f:
            for row in csv.DictReader(f):
                if row["email"] == email and row["password"] == password:
                    init_prediction_state()
                    session["user"] = email
                    session.permanent = True
                    return redirect(url_for("dashboard"))

        return render_template("auth.html", error="Invalid credentials")

    return render_template("auth.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        with open(USERS_FILE, "a", newline="") as f:
            csv.writer(f).writerow([
                request.form.get("email"),
                request.form.get("password")
            ])
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/guest")
def guest_login():
    init_prediction_state()
    session["user"] = "guest@jobai.com"
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===============================
# PAGES
# ===============================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/analytics")
@login_required
@prediction_required
def analytics():
    return render_template("analytics.html")


@app.route("/history")
@login_required
def history():
    return render_template(
        "history.html",
        predictions=get_last_10_predictions()
    )


@app.route("/skill-gap")
@login_required
@prediction_required
def skill_gap():
    return render_template("skill-gap.html")


@app.route("/chatbot")
@login_required
@prediction_required
def chatbot():
    return render_template("chatbot.html")

# ===============================
# 🔥 PREDICTION API
# ===============================
@app.route("/predict", methods=["POST"])
@login_required
def predict():
    data = request.get_json(force=True)

    jobtitle = data.get("jobtitle", "").lower().strip()
    location = data.get("location", "").lower().strip()
    experience = data.get("experience_level", "").strip()
    industry = data.get("industry", "").lower().strip()
    skills = data.get("required_skills", "").lower().strip()

    demand, confidence, career_risk, ai_probability = predict_job_demand(
        jobtitle, location, experience, industry, skills
    )

    skill_count = len([s for s in skills.split(",") if s.strip()])

    if demand == "High":
        decision = "Good time to switch"
        trend = [55, 60, 65, 70, 75]
    elif demand == "Medium":
        decision = "Switch with preparation"
        trend = [42, 45, 47, 50, 52]
    else:
        decision = "Not recommended currently"
        trend = [35, 32, 30, 28, 26]

    save_prediction_to_db({
        "jobtitle": jobtitle,
        "location": location,
        "experience_level": experience,
        "industry": industry,
        "skill_count": skill_count,
        "demand": demand,
        "confidence": confidence
    })

    session.update({
        "prediction_done": True,
        "user_input": {
            "jobtitle": jobtitle,
            "location": location,
            "experience_level": experience,
            "industry": industry,
            "skills": skills
        },
        "demand": demand,
        "career_risk": career_risk,
        "ai_probability": ai_probability,
        "confidence": confidence,
        "career_decision": decision,
        "demand_trend": trend,
        "volatility_trend": [22, 30, 26, 34, 28, 38]
    })

    return jsonify({"status": "ok"})

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
