import requests
import os

# Configuration
BASE_URL = os.environ.get('APP_URL', 'http://localhost:5000')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'your_secure_token_here')

def test_remote_publish():
    endpoint = f"{BASE_URL}/api/post"
    
    payload = {
        "title": "Docker Deployment Test",
        "content": "Checking if the containerized app accepts writes."
    }
    
    headers = {
        "X-Admin-Token": ADMIN_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        print(f"Sending POST request to {endpoint}...")
        response = requests.post(endpoint, json=payload, headers=headers)
        
        if response.status_code == 201:
            print("✅ SUCCESS: Post published.")
            print("Response:", response.json())
        elif response.status_code == 401:
            print("❌ FAILED: Unauthorized. Check your ADMIN_TOKEN.")
        else:
            print(f"⚠️ FAILED: Status Code {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect. Is the Docker container running?")

if __name__ == "__main__":
    test_remote_publish()