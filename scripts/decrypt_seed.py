from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )

def decrypt_seed():
    # Read encrypted seed (base64)
    with open("encrypted_seed.txt", "r") as f:
        encrypted_b64 = f.read().strip()

    encrypted_bytes = base64.b64decode(encrypted_b64)

    private_key = load_private_key()

    print("Decrypting with RSA-OAEP-SHA256...")

    try:
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        print("\n❌ Decryption FAILED!")
        print(e)
        return

    seed_hex = decrypted_bytes.decode().strip()

    if len(seed_hex) != 64:
        print("\n❌ Seed length wrong. Expected 64-char hex.")
        print("Got:", seed_hex)
        return

    print("\n✔ Decrypted Seed =", seed_hex)

    # Save seed
    with open("seed.txt", "w") as f:
        f.write(seed_hex)

    print("\n✔ Seed saved to seed.txt")

if __name__ == "__main__":
    decrypt_seed()
