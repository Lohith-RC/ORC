import requests
import os
import uuid
from pathlib import Path

# Define backend URL
url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Generate unique username to ensure registration works
unique_username = f"user_{uuid.uuid4().hex[:8]}"
register_data = {
    "username": unique_username,
    "password": "testpassword",
    "full_name": "Test User",
    "email": f"{unique_username}@example.com"
}

print(f"Attempting to register user: {unique_username}")
response = requests.post(f"{url}/register", json=register_data)
if response.status_code == 200:
    print(f"Register status: {response.status_code}, Response: {response.json()}")
else:
    print(f"Registration failed: {response.status_code}, {response.text}")
    # Try to proceed if it already exists (unlikely with UUID but safe)

# Step 2: Login to get token
login_data = {
    "username": unique_username,
    "password": "testpassword"
}
response = requests.post(f"{url}/login", data=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"Login successful. Token acquired.")
else:
    print(f"Login failed: {response.status_code}, {response.text}")
    exit()

# Step 3: Perform a prediction with a sample image
headers = {"Authorization": f"Bearer {token}"}
base_dir = Path(__file__).resolve().parent
image_path = base_dir / "data_split" / "test" / "cancer" / "010.jpeg"

if image_path.exists():
    with image_path.open("rb") as f:
        files = {"file": ("010.jpeg", f, "image/jpeg")}
        print(f"Sending image for prediction: {image_path}")
        response = requests.post(f"{url}/predict", headers=headers, files=files)
        if response.status_code == 200:
            print("\n--- PREDICTION OUTPUT ---")
            data = response.json()
            print(f"Prediction: {data['prediction']}")
            print(f"Confidence: {data['confidence']:.4f}")
            print("--------------------------")
        else:
            print(f"Prediction failed: {response.status_code}, {response.text}")
else:
    print(f"Sample image not found at {image_path}")
