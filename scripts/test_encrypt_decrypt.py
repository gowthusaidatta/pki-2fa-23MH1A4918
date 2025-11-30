# scripts/test_encrypt_decrypt.py
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path

pub = Path("student_public.pem").read_bytes()
priv = Path("student_private.pem").read_bytes()

from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
pubk = load_pem_public_key(pub)
privk = load_pem_private_key(priv, password=None)

plaintext = b"0123456789abcdef0123456789abcdef"  # 32 bytes hex-looking
ct = pubk.encrypt(
    plaintext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
print("encrypted (base64):", base64.b64encode(ct).decode())
pt = privk.decrypt(
    ct,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
print("decrypted repr:", repr(pt))
print("decrypted str:", pt.decode())
