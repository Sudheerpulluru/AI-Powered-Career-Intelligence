# Job Market Analytics & Job Demand Prediction System

A machine learning based analytics and prediction system that analyzes job market data and predicts job demand levels (Low / Medium / High).  
The project implements a complete end-to-end ML pipeline with statistical validation, business optimization, and a Flask-based web application.

---

## Project Highlights
- End-to-end machine learning pipeline
- Baseline vs advanced model comparison
- Hyperparameter tuning
- Statistical validation using Paired T-Test
- Business impact based threshold optimization
- Interactive Flask web application

---

## Technologies Used
- Python
- Pandas, NumPy
- Scikit-learn
- Joblib
- Matplotlib
- Flask
- SQLite
- HTML, CSS, Bootstrap

---

## System Architecture
User Input → Data Preprocessing → ML Model → Statistical Validation → Business Optimization → Prediction Output

---

## Project Structure

Job-Market-Analytics/
│
├── app.py
├── main.py
├── database.db
├── requirements.txt
├── README.md
│
├── data/
├── notebooks/
├── results/
├── src/
│   └── models/
│       ├── demand_predictor.py
│       └── statistical_validation.py
│
├── static/
└── templates/

---

## Installation & Setup

1. Create virtual environment  
   python -m venv venv

2. Activate virtual environment (Windows)  
   venv\Scripts\activate

3. Install dependencies  
   pip install -r requirements.txt

---

## How to Run

Run full ML pipeline:
python main.py

Run web application:
python app.py

Open in browser:
http://127.0.0.1:5000

---

## Machine Learning Workflow
1. Data preprocessing
2. Feature engineering
3. Baseline model comparison
4. Advanced model training
5. Hyperparameter tuning
6. Statistical validation
7. Business optimization
8. Deployment using Flask

---

## Statistical Validation
- Cross-validation performed on baseline and tuned models
- Paired T-Test used for significance testing
- Result: Improvement observed but NOT statistically significant

---

## Business Optimization
The prediction threshold is selected based on expected business impact rather than accuracy alone, ensuring safer and more practical decisions.

---

## Sample Output

Job Title        : AI Engineer  
Location         : India  
Experience       : 2–5 years  
Industry         : Software  
Skills           : Python, Machine Learning, AWS  

Predicted Demand : High  
Confidence Score : 85%  
Career Risk      : Low  
AI Exposure      : 30%  

---

## Limitations
- Depends on historical data
- No real-time job data integration
- Limited feature set

---

## Future Enhancements
- Real-time job portal integration
- Deep learning models
- Resume-based recommendations
- Cloud deployment

---

## Academic Details
Project Type: Final Year B.Tech Project  
Domain: Machine Learning & Data Analytics  

---

## License
This project is developed for academic purposes.
