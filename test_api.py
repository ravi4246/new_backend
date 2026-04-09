import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"

def test_registration():
    url = BASE_URL + "register/"
    data = {
        "phone": "9876543211",
        "password": "testpass123",
        "email": "test_drf@example.com",
        "profile": {
            "full_name": "DRF Test User",
            "age": 30,
            "gender": "Male",
            "blood_group": "A+",
            "phone": "9876543211"
        }
    }
    response = requests.post(url, json=data)
    print(f"Registration Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 201

def test_token():
    url = BASE_URL + "token/"
    data = {
        "phone": "9876543211",
        "password": "testpass123"
    }
    response = requests.post(url, json=data)
    print(f"Token Status: {response.status_code}")
    if response.status_code == 200:
        return response.json()['access']
    return None

if __name__ == "__main__":
    if test_registration():
        token = test_token()
        if token:
            print("Successfully registered and obtained token.")
        else:
            print("Failed to obtain token.")
    else:
        # Try getting token anyway if user exists
        token = test_token()
        if token:
            print("User already exists, obtained token.")
        else:
            print("Test failed.")
