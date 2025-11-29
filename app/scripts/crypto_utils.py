import base64
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

PRIVATE_KEY_PATH = Path("student_private.pem")


def load_private_key():
    """Load student's RSA private key"""
    if not PRIVATE_KEY_PATH.exists():
        raise FileNotFoundError(f"Private key not found: {PRIVATE_KEY_PATH}")

    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)


def decrypt_seed(encrypted_seed: str) -> str:
    """Decrypts Base64-encoded RSA encrypted seed"""
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

        seed = decrypted_bytes.decode()

        if len(seed) != 32 or not all(c in "0123456789abcdef" for c in seed.lower()):
            raise ValueError("Invalid seed format")

        return seed

    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
