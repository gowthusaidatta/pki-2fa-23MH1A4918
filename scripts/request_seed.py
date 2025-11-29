import json
import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

STUDENT_ID = "23MH1A4918"
GITHUB_REPO_URL = "https://github.com/gowthusaidatta/pki-2fa-23MH1A4918"


def load_public_key():
    with open("student_public.pem", "r") as f:
        return f.read()


def request_encrypted_seed():
    pubkey = load_public_key()

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": pubkey
    }

    print("\nSending request to Instructor API...\n")

    response = requests.post(API_URL, json=payload)
    data = response.json()

    print("\nResponse:\n", json.dumps(data, indent=4))

    if "encrypted_seed" in data:
        with open("encrypted_seed.txt", "w") as f:
            f.write(data["encrypted_seed"])
        print("✔ Saved encrypted_seed.txt")
    else:
        print("❌ Failed: encrypted_seed missing")


if __name__ == "__main__":
    request_encrypted_seed()
