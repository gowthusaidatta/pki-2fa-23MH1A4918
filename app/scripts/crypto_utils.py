from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load student's private key (the file that exists)
with open("app/student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

def decrypt_seed(enc_b64):
    import base64
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    cipher_bytes = base64.b64decode(enc_b64)

    key = b"thisisaverysecretkey1234567890!!"[:32]   # 32 bytes AES-256
    iv = cipher_bytes[:16]
    ciphertext = cipher_bytes[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    seed = decryptor.update(ciphertext) + decryptor.finalize()

    return seed.rstrip(b"\x00")


def sign_message(message: str) -> str:
    signature = private_key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature.hex()
