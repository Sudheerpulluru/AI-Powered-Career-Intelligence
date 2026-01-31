from predict import predict_demand

# ===============================
# BASE DATA POOLS
# ===============================
high_roles = [
    "Software Engineer", "Full Stack Developer", "Data Scientist",
    "ML Engineer", "DevOps Engineer", "Cloud Engineer",
    "AI Engineer", "Cyber Security Analyst", "Product Manager"
]

medium_roles = [
    "Data Analyst", "Business Analyst", "QA Engineer",
    "Network Engineer", "System Administrator", "UI UX Designer",
    "Game Developer", "Blockchain Consultant", "Support Engineer"
]

low_roles = [
    "Mechanical Engineer", "Civil Engineer", "Chemical Engineer",
    "Bioinformatics Engineer", "HR Analyst", "Finance Analyst",
    "Research Scientist", "Electrical Engineer"
]

high_cities = ["Bangalore", "Hyderabad", "Pune"]
other_cities = ["Mumbai", "Delhi", "Chennai", "Vizag"]

experiences = ["Fresher", "1 year", "2 years", "3-5 years", "5+ years"]
industries = ["IT", "Analytics", "Research", "Manufacturing", "Finance"]
skills = ["python", "java", "sql", "ml", "cloud", "excel"]

# ===============================
# GENERATE 100 TEST CASES
# ===============================
test_cases = []

# 1️⃣ High demand cases (40)
for role in high_roles:
    for city in high_cities:
        test_cases.append(
            (role, city, "3 years", "IT", "python, sql", "High")
        )
        if len(test_cases) >= 40:
            break
    if len(test_cases) >= 40:
        break

# 2️⃣ Medium demand cases (35)
for role in medium_roles:
    for city in high_cities + other_cities:
        test_cases.append(
            (role, city, "2 years", "IT", "sql, excel", "Medium")
        )
        if len(test_cases) >= 75:
            break
    if len(test_cases) >= 75:
        break

# 3️⃣ Low demand cases (25)
for role in low_roles:
    for city in other_cities:
        test_cases.append(
            (role, city, "4 years", "Manufacturing", "autocad", "Low")
        )
        if len(test_cases) >= 100:
            break
    if len(test_cases) >= 100:
        break

# ===============================
# RUN AUTOMATED TESTS
# ===============================
print("\n🔍 AUTOMATED TESTING (100 TEST CASES) STARTED\n")

pass_count = 0

for i, tc in enumerate(test_cases, start=1):
    result = predict_demand(*tc[:-1])
    expected = tc[-1]

    status = "PASS ✅" if result == expected else "FAIL ❌"
    if status.startswith("PASS"):
        pass_count += 1

    print(f"TC{i:03d}: Expected={expected}, Got={result} → {status}")

print(f"\n✅ {pass_count}/100 Test Cases Passed")
print("🏁 Automated Testing Completed")
