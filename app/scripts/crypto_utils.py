# app/scripts/crypto_utils.py
import base64
import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Accept several likely paths so Docker vs. local works
CANDIDATE_PRIVATE_PATHS = [
    Path("/app/student_private.pem"),           # docker recommended path
    Path("/app/scripts/student_private.pem"),
    Path("student_private.pem"),
    Path("app/scripts/student_private.pem"),
    Path("app/student_private.pem"),
]

def find_private_key_path():
    for p in CANDIDATE_PRIVATE_PATHS:
        if p.exists():
            return p
    raise FileNotFoundError("student_private.pem not found in expected locations.")

def load_private_key():
    key_path = find_private_key_path()
    with open(key_path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_seed(encrypted_seed: str) -> str:
    """
    Decrypt Base64 RSA-OAEP(SHA256) encrypted seed and validate format.
    Returns 64-char hex string.
    Raises ValueError on failure.
    """
    try:
        private_key = load_private_key()
        encrypted_bytes = base64.b64decode(encrypted_seed)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        seed = decrypted_bytes.decode("utf-8").strip()

        # Validation: 64 hex characters
        if len(seed) != 64:
            raise ValueError(f"Invalid seed length: {len(seed)} (expected 64)")
        if not all(c in "0123456789abcdef" for c in seed.lower()):
            raise ValueError("Seed contains non-hex characters")

        return seed

    except Exception as exc:
        # raise ValueError to be caught by main and converted to 500
        raise ValueError(f"Decryption failed: {exc}")
