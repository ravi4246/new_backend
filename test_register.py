import requests

# We know John Doe exists. Let's create a brand new user and log in to test.
base_url = "http://127.0.0.1:8000/api"

register_data = {
    "phone": "5551234999",
    "password": "password123",
    "email": "test999@example.com",
    "profile": {
        "full_name": "Test Testerson",
        "age": 35,
        "gender": "Female",
        "blood_group": "A+",
        "phone": "5551234999",
        "initial_symptoms": "headache",
        "initial_sleep": "good",
        "initial_digestion": "good",
        "initial_activity": "moderate",
        "habits": "none"
    }
}

try:
    reg_resp = requests.post(f"{base_url}/register/", json=register_data)
    
    login_resp = requests.post(f"{base_url}/token/", json={"phone": "5551234999", "password": "password123"})
    token = login_resp.json().get('access')
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try PUT with partial missing data (simulate GSON stripping nulls)
    put_data = {
        "full_name": "Test Missing Keys",
        "gender": "Male",
        "blood_group": "B+"
        # omitted age, phone, symptoms, sleep, etc.
    }
    put_resp = requests.put(f"{base_url}/profile/", json=put_data, headers=headers)
    print("PUT MISSING KEYS:", put_resp.status_code, put_resp.text)
    
    # And GET
    get_resp = requests.get(f"{base_url}/profile/", headers=headers)
    print("GET:", get_resp.status_code, get_resp.text)
    
except Exception as e:
    print(e)
    # the server might not be running locally in this container, but we can query Django directly anyway.

