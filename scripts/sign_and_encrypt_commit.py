import hashlib
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

ROLL = "23MH1A4918"

def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_instructor_public_key():
    with open("instructor_public.pem", "rb") as f:
        return serialization.load_pem_public_key(f.read())

def load_seed():
    with open("seed.txt", "r") as f:
        return f.read().strip()

def main():
    print("🔐 Loading keys and seed...\n")

    private_key = load_private_key()
    instructor_pub = load_instructor_public_key()
    seed = load_seed()

    print(f"✔ Seed loaded = {seed}")

    # Prepare commit data
    commit_data = {
        "roll": ROLL,
        "seed": seed
    }
    commit_json = json.dumps(commit_data).encode()

    # -----------------------------------------------------------
    # STEP 1: SIGN THE COMMIT JSON USING STUDENT PRIVATE KEY
    # -----------------------------------------------------------
    signature = private_key.sign(
        commit_json,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=32
        ),
        hashes.SHA256()
    )

    with open("commit_signature.hex", "w") as f:
        f.write(signature.hex())

    print("\n✔ Signature created (saved to commit_signature.hex)\n")

    # -----------------------------------------------------------
    # STEP 2: ENCRYPT THE COMMIT USING INSTRUCTOR PUBLIC KEY
    # -----------------------------------------------------------
    encrypted = instructor_pub.encrypt(
        commit_json,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("encrypted_commit.bin", "wb") as f:
        f.write(encrypted)

    print("✔ Commit encrypted (saved to encrypted_commit.bin)\n")

    print("🎉 STEP 1 COMPLETE — Send these two files:")
    print("    - commit_signature.hex")
    print("    - encrypted_commit.bin")

if __name__ == "__main__":
    main()
