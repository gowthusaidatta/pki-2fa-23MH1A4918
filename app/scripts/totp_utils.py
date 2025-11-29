import hmac
import time
import base64
import struct
import hashlib


def generate_totp(secret_hex: str) -> str:
    key = bytes.fromhex(secret_hex)
    counter = int(time.time() // 30)

    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()

    offset = h[-1] & 0x0F
    code = (struct.unpack(">I", h[offset:offset+4])[0] & 0x7fffffff) % 1000000

    return f"{code:06d}"


def verify_totp(secret_hex: str, user_code: str) -> bool:
    return user_code == generate_totp(secret_hex)
