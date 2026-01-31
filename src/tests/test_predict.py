from predict import predict_demand

test_cases = [
    # jobtitle, city, experience, industry, skills, expected
    ("Software Engineer", "Bangalore", "2-5 years", "IT", "java, sql", "High"),
    ("Software Engineer", "Hyderabad", "3 years", "IT", "python", "High"),
    ("Data Scientist", "Bangalore", "2 years", "IT", "ml, python", "High"),
    ("Full Stack Developer", "Pune", "4 years", "IT", "react, node", "High"),
    ("Data Analyst", "Hyderabad", "1-3 years", "Analytics", "excel, power bi", "Medium"),
    ("Data Analyst", "Mumbai", "2 years", "Analytics", "sql", "Low"),
    ("Bioinformatics Engineer", "Pune", "5 years", "Healthcare", "genomics", "Low"),
    ("Mechanical Engineer", "Chennai", "3 years", "Manufacturing", "autocad", "Low"),
    ("AI Ethics Officer", "Delhi", "2 years", "Research", "policy", "Low"),
    ("Java Developer", "Bangalore", "3 years", "IT", "spring, sql", "High")
]

print("\n🔍 AUTOMATED TESTING STARTED\n")

pass_count = 0

for i, tc in enumerate(test_cases, start=1):
    result = predict_demand(*tc[:-1])
    expected = tc[-1]

    status = "PASS ✅" if result == expected else "FAIL ❌"

    if status.startswith("PASS"):
        pass_count += 1

    print(f"TC{i}: Expected={expected}, Got={result} → {status}")

print(f"\n✅ {pass_count}/10 Test Cases Passed")
print("🏁 Automated Testing Completed")
