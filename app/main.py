import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scripts.crypto_utils import decrypt_seed
from scripts.totp_utils import generate_totp, verify_totp



DATA_PATH = "/data/seed.txt"

app = FastAPI(title="FastAPI 2FA", version="1.0.0")


# -------------------------------
# Request Models
# -------------------------------
class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# -------------------------------
# Helper: Load Seed Securely
# -------------------------------
def load_seed():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Seed not decrypted yet")

    with open(DATA_PATH, "r") as f:
        return f.read().strip()


# -------------------------------
# POST /decrypt-seed
# -------------------------------
@app.post("/decrypt-seed")
def api_decrypt_seed(data: DecryptRequest):
    try:
        # 1. Decrypt seed
        seed_hex = decrypt_seed(data.encrypted_seed)

        # 2. Persist seed at /data/seed.txt
        os.makedirs("/data", exist_ok=True)
        with open(DATA_PATH, "w") as f:
            f.write(seed_hex)

        return {"status": "ok", "seed": seed_hex}


    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")


# -------------------------------
# GET /generate-2fa
# -------------------------------
@app.get("/generate-2fa")
def api_generate_2fa():
    try:
        seed_hex = load_seed()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Generate TOTP and seconds left
    code, valid_for = generate_totp(seed_hex)

    return {
        "code": code,
        "valid_for": valid_for
    }


# -------------------------------
# POST /verify-2fa
# -------------------------------
@app.post("/verify-2fa")
def api_verify_2fa(data: VerifyRequest):
    # Validate input
    if not data.code:
        raise HTTPException(status_code=400, detail="Missing code")

    try:
        seed_hex = load_seed()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Verify with ±1 time window
    is_valid = verify_totp(seed_hex, data.code)

    return {"valid": is_valid}
