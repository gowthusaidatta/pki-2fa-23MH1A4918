from fastapi import FastAPI
from pydantic import BaseModel

from app.scripts.crypto_utils import decrypt_seed, sign_message
from app.scripts.totp_utils import totp
app = FastAPI()

# Load encrypted seed
encrypted_seed = open("app/encrypted_seed.txt").read().strip()
seed_bytes = decrypt_seed(encrypted_seed)

# Convert bytes → hex
seed_hex = seed_bytes.hex()


@app.get("/totp")
def get_totp():
    return {"totp": totp(seed_hex)}


@app.get("/sign")
def sign_current_totp():
    current_totp = totp(seed_hex)
    sig = sign_message(current_totp)
    return {"totp": current_totp, "signature": sig}


class SubmitRequest(BaseModel):
    roll: str
    totp: str
    signature: str
    public_key: str


@app.post("/submit")
def submit(data: SubmitRequest):
    correct = totp(seed_hex)

    if data.totp != correct:
        return {"status": "error", "message": "Invalid TOTP"}

    package = data.dict()

    with open("app/last_submission.json", "w") as f:
        import json
        json.dump(package, f, indent=4)

    return {"status": "success", "payload": package}
