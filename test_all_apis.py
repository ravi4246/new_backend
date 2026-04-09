import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000/api/"

def run_tests():
    print("Starting API Tests...\n" + "="*40)
    
    # Generate unique test data
    unique_id = str(uuid.uuid4())[:8]
    test_phone = f"999{unique_id[:7]}"
    test_email = f"test_{unique_id}@example.com"
    test_password = "securepassword123"

    # --- 1. Registration ---
    print(f"\n[1] Testing Registration for {test_phone}...")
    reg_url = BASE_URL + "register/"
    reg_data = {
        "phone": test_phone,
        "password": test_password,
        "email": test_email,
        "profile": {
            "full_name": f"Test User {unique_id}",
            "age": 25,
            "gender": "Other",
            "blood_group": "O+",
            "phone": test_phone
        }
    }
    reg_response = requests.post(reg_url, json=reg_data)
    if reg_response.status_code != 201:
        print(f"[FAIL] Registration Failed. Status: {reg_response.status_code}")
        print(reg_response.text)
        return
    print("[OK] Registration Successful.")

    # --- 2. Authentication (Get Token) ---
    print("\n[2] Testing Authentication...")
    token_url = BASE_URL + "token/"
    token_data = {"phone": test_phone, "password": test_password}
    token_response = requests.post(token_url, json=token_data)
    
    if token_response.status_code != 200:
        print(f"[FAIL] Authentication Failed. Status: {token_response.status_code}")
        print(token_response.text)
        return
    
    access_token = token_response.json().get('access')
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    print("[OK] Authentication Successful. Token acquired.")

    # --- 3. Profile API ---
    print("\n[3] Testing Profile API...")
    profile_url = BASE_URL + "profile/"
    profile_response = requests.get(profile_url, headers=headers)
    if profile_response.status_code == 200:
        print("[OK] Profile API works:")
        print(json.dumps(profile_response.json(), indent=2))
    else:
        print(f"[FAIL] Profile API Failed. Status: {profile_response.status_code}")

    # --- 4. Health Logs API ---
    print("\n[4] Testing Health Logs API (Create)...")
    health_url = BASE_URL + "health-logs/"
    health_data = {
        "heart_rate": 72,
        "blood_pressure": "120/80",
        "sleep_hours": 7.5,
        "stress_level": "Low",
        "diet_notes": "Healthy breakfast",
        "exercise_minutes": 30,
        "symptoms": "Feeling fine",
        "sleep_quality": 8,
        "digestion_status": "Normal",
        "activity_level": "Moderate"
    }
    health_response = requests.post(health_url, headers=headers, json=health_data)
    if health_response.status_code == 201:
        print("[OK] Health Log created successfully.")
    else:
        print(f"[FAIL] Health Log creation failed. Status: {health_response.status_code}")
        print(health_response.text)

    # --- 5. Therapy Plans API ---
    print("\n[5] Testing Therapy Plans API (Get)...")
    therapy_url = BASE_URL + "therapy-plans/"
    therapy_response = requests.get(therapy_url, headers=headers)
    if therapy_response.status_code == 200:
        print("[OK] Therapy Plans API works.")
    else:
        print(f"[FAIL] Therapy Plans API failed. Status: {therapy_response.status_code}")

    # --- 6. AI Analysis API ---
    print("\n[6] Testing AI Analysis API...")
    ai_url = BASE_URL + "analysis/"
    try:
        # Note: Analysis view currently accepts GET request without auth in the code, but it's good practice to try with headers.
        ai_response = requests.get(ai_url, headers=headers)
        if ai_response.status_code == 200:
            print("[OK] AI Analysis API works:")
            print(json.dumps(ai_response.json(), indent=2))
        else:
            print(f"[FAIL] AI Analysis API Failed. Status: {ai_response.status_code}")
            print(ai_response.text)
    except Exception as e:
        print(f"[FAIL] AI Analysis API Failed due to error: {e}")

    print("\n" + "="*40 + "\nTesting Completed.")

if __name__ == "__main__":
    try:
        # Check if server is reachable first
        requests.get(BASE_URL.replace("api/", ""))
        run_tests()
    except requests.exceptions.ConnectionError:
        print("[FAIL] ERROR: Cannot connect to the server. Is it running?")
        print("Please start the server first: .\\venv\\Scripts\\python.exe manage.py runserver")
