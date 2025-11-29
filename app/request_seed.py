import json
import base64
import requests

STUDENT_ID = "23MH1A4918"
REPO_URL = "https://github.com/gowthusaidatta/pki-2fa-23MH1A4918"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

# Read public key
with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": REPO_URL,
    "public_key": public_key
}

print("Sending request to instructor API...")
response = requests.post(API_URL, json=payload)
print("Response status:", response.status_code)

data = response.json()
print("Response:", data)

if "encrypted_seed" in data:
    with open("encrypted_seed.txt", "w") as f:
        f.write(data["encrypted_seed"])
    print("\nEncrypted seed saved to encrypted_seed.txt")
else:
    print("\nFailed to receive encrypted seed.")
