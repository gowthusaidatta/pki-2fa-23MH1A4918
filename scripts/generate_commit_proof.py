import base64
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Load keys
def load_private_key(path):
    return serialization.load_pem_private_key(open(path, "rb").read(), password=None)

def load_public_key(path):
    return serialization.load_pem_public_key(open(path, "rb").read())

# Sign using RSA-PSS-SHA256
def sign_commit_hash(commit_hash, private_key):
    return private_key.sign(
        commit_hash.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# HASH THE SIGNATURE — IMPORTANT FIX
def shrink_signature(signature_bytes):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(signature_bytes)
    return digest.finalize()   # 32 bytes

# Encrypt using RSA-OAEP-SHA256
def encrypt_signature(signature_hash, public_key):
    return public_key.encrypt(
        signature_hash,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

if __name__ == "__main__":
    commit_hash = sys.argv[1]

    student_private = load_private_key("student_private.pem")
    instructor_public = load_public_key("instructor_public.pem")

    # Step 1: Create RSA-PSS signature
    signature = sign_commit_hash(commit_hash, student_private)

    # Step 2: Hash the signature (Fix for OAEP size limit)
    signature_hash = shrink_signature(signature)

    # Step 3: Encrypt the hash
    encrypted = encrypt_signature(signature_hash, instructor_public)

    # Step 4: Print base64
    print(base64.b64encode(encrypted).decode())
