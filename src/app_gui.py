import tkinter as tk
import joblib
import pandas as pd

model = joblib.load("data/job_demand_model.pkl")
encoder = joblib.load("data/label_encoder.pkl")
skills_df = pd.read_csv("data/skill_demand.csv")
skills = skills_df['skill'].tolist()

def predict():
    desc = entry.get().lower()
    skill_score = sum(1 for s in skills if s in desc)

    X = pd.DataFrame([[skill_score, 1, 1]],
                     columns=['skill_score', 'role_score', 'location_score'])

    result = encoder.inverse_transform(model.predict(X))[0]
    output.config(text="Predicted Demand: " + result)

app = tk.Tk()
app.title("Job Demand Predictor")

tk.Label(app, text="Enter Job Description").pack()
entry = tk.Entry(app, width=60)
entry.pack()

tk.Button(app, text="Predict", command=predict).pack()
output = tk.Label(app, text="")
output.pack()

app.mainloop()
