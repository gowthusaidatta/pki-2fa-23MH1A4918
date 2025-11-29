import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# --------------------------
# DECRYPT SEED (AES-CBC)
# --------------------------

def decrypt_seed(enc_b64: str) -> bytes:
    cipher_bytes = base64.b64decode(enc_b64)

    key = b"MYSUPERSECRETKEY123"[:16]    # MUST match your AES key used during encryption
    iv = cipher_bytes[:16]
    encrypted = cipher_bytes[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(encrypted) + decryptor.finalize()

    pad_len = padded[-1]
    seed_bytes = padded[:-pad_len]
    return seed_bytes


# --------------------------
# LOAD PRIVATE KEY
# --------------------------

with open("app/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# --------------------------
# SIGN MESSAGE (RSA)
# --------------------------

def sign_message(message: str) -> str:
    signature = private_key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()
