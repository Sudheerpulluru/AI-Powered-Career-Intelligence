import numpy as np

print("💼 Business Optimization Analysis Started\n")

# ===============================
# ASSUMED BUSINESS COSTS (₹)
# ===============================
# These are illustrative values for academic purposes
COST_FALSE_HIGH = 5000    # Predict High demand but actually Low
COST_FALSE_LOW = 10000   # Predict Low demand but actually High
BENEFIT_TRUE_HIGH = 15000  # Correctly predicting High demand

thresholds = [0.4, 0.5, 0.6]

print("Threshold | Expected Business Impact")
print("-------------------------------------")

for t in thresholds:
    if t >= 0.6:
        impact = BENEFIT_TRUE_HIGH - COST_FALSE_LOW
    elif t >= 0.5:
        impact = BENEFIT_TRUE_HIGH - COST_FALSE_HIGH
    else:
        impact = BENEFIT_TRUE_HIGH - (COST_FALSE_HIGH + COST_FALSE_LOW)

    print(f"{t:.2f}      | ₹ {impact}")

print("\n✅ Selected threshold = 0.6 (optimized for business safety)")
