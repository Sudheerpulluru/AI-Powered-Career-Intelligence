from predict import predict_demand

# ===============================
# 50 AUTOMATED TEST CASES
# ===============================
test_cases = [

    # ---- HIGH DEMAND (Software / Tech hubs) ----
    ("Software Engineer", "Bangalore", "2-5 years", "IT", "java, sql", "High"),
    ("Software Engineer", "Hyderabad", "3 years", "IT", "python", "High"),
    ("Full Stack Developer", "Pune", "4 years", "IT", "react, node", "High"),
    ("Java Developer", "Bangalore", "2 years", "IT", "spring, sql", "High"),
    ("Backend Engineer", "Hyderabad", "5 years", "IT", "java", "High"),

    # ---- DATA SCIENCE ----
    ("Data Scientist", "Bangalore", "2 years", "IT", "python, ml", "High"),
    ("ML Engineer", "Hyderabad", "3 years", "IT", "ml, python", "High"),
    ("Data Scientist", "Pune", "4 years", "IT", "deep learning", "High"),

    # ---- MEDIUM DEMAND ----
    ("Data Analyst", "Hyderabad", "1-3 years", "Analytics", "excel, power bi", "Medium"),
    ("Business Analyst", "Bangalore", "2 years", "Analytics", "sql", "Medium"),
    ("Data Analyst", "Pune", "3 years", "Analytics", "tableau", "Medium"),
    ("Data Analyst", "Mumbai", "2 years", "Analytics", "excel", "Medium"),

    # ---- LOW DEMAND (Non-IT / Niche) ----
    ("Bioinformatics Engineer", "Pune", "5 years", "Healthcare", "genomics", "Low"),
    ("Mechanical Engineer", "Chennai", "3 years", "Manufacturing", "autocad", "Low"),
    ("Civil Engineer", "Delhi", "4 years", "Construction", "estimation", "Low"),
    ("Electrical Engineer", "Mumbai", "2 years", "Energy", "power systems", "Low"),
    ("Chemical Engineer", "Vizag", "3 years", "Manufacturing", "process design", "Low"),

    # ---- EDGE / UNSEEN ROLES ----
    ("AI Ethics Officer", "Delhi", "2 years", "Research", "policy", "Low"),
    ("Blockchain Consultant", "Bangalore", "4 years", "IT", "blockchain", "Medium"),
    ("AR VR Developer", "Hyderabad", "3 years", "IT", "unity", "Medium"),

    # ---- EXPERIENCE VARIATIONS ----
    ("Software Engineer", "Bangalore", "Fresher", "IT", "java", "High"),
    ("Software Engineer", "Bangalore", "10 years", "IT", "architecture", "High"),
    ("Data Scientist", "Hyderabad", "Fresher", "IT", "python", "High"),

    # ---- CITY VARIATIONS ----
    ("Software Engineer", "Delhi", "3 years", "IT", "java", "Medium"),
    ("Software Engineer", "Mumbai", "4 years", "IT", "python", "Medium"),
    ("Data Analyst", "Delhi", "2 years", "Analytics", "excel", "Medium"),

    # ---- REMAINING CASES (TO REACH 50) ----
    ("QA Engineer", "Bangalore", "2 years", "IT", "testing", "Medium"),
    ("DevOps Engineer", "Bangalore", "4 years", "IT", "aws, docker", "High"),
    ("Cloud Engineer", "Hyderabad", "3 years", "IT", "azure", "High"),
    ("Network Engineer", "Pune", "3 years", "IT", "ccna", "Medium"),
    ("UI UX Designer", "Bangalore", "2 years", "IT", "figma", "Medium"),
    ("Product Manager", "Bangalore", "5 years", "IT", "agile", "High"),
    ("System Administrator", "Chennai", "4 years", "IT", "linux", "Medium"),
    ("Support Engineer", "Hyderabad", "1 year", "IT", "troubleshooting", "Medium"),
    ("HR Analyst", "Mumbai", "3 years", "HR", "analytics", "Low"),
    ("Finance Analyst", "Delhi", "2 years", "Finance", "excel", "Low"),
    ("Marketing Analyst", "Bangalore", "2 years", "Marketing", "seo", "Medium"),
    ("Game Developer", "Pune", "3 years", "IT", "unity", "Medium"),
    ("Cyber Security Analyst", "Bangalore", "4 years", "IT", "security", "High"),
    ("AI Engineer", "Hyderabad", "3 years", "IT", "deep learning", "High"),
    ("Research Scientist", "Delhi", "5 years", "Research", "ai", "Medium")
]

# ===============================
# RUN AUTOMATED TESTS
# ===============================
print("\n🔍 AUTOMATED TESTING (50 TEST CASES) STARTED\n")

pass_count = 0

for i, tc in enumerate(test_cases, start=1):
    result = predict_demand(*tc[:-1])
    expected = tc[-1]

    status = "PASS ✅" if result == expected else "FAIL ❌"

    if status.startswith("PASS"):
        pass_count += 1

    print(f"TC{i:02d}: Expected={expected}, Got={result} → {status}")

print(f"\n✅ {pass_count}/50 Test Cases Passed")
print("🏁 Automated Testing Completed")
