from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.scripts.crypto_utils import decrypt_seed
from app.scripts.totp_utils import generate_totp, verify_totp

app = FastAPI(title="FastAPI 2FA")

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    seed: str
    code: str


@app.post("/decrypt-seed")
def decrypt_seed_api(req: DecryptRequest):
    try:
        seed = decrypt_seed(req.encrypted_seed)
        return {"seed": seed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate-2fa")
def generate_code(seed: str):
    try:
        return generate_totp(seed)
    except:
        raise HTTPException(status_code=500, detail="Invalid seed")


@app.post("/verify-2fa")
def verify_code(req: VerifyRequest):
    try:
        ok = verify_totp(req.seed, req.code)
        return {"valid": ok}
    except:
        raise HTTPException(status_code=500, detail="Verification error")
