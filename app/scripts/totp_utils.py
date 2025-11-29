import base64
import time
import hmac
import struct
import hashlib

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode().replace("=", "")
    return base32_seed

def generate_totp(hex_seed: str, for_time=None) -> str:
    if for_time is None:
        for_time = int(time.time())

    time_step = 30
    counter = int(for_time / time_step)

    base32_seed = hex_to_base32(hex_seed)
    key = base64.b32decode(base32_seed + "====", casefold=True)

    msg = struct.pack(">Q", counter)

    h = hmac.new(key, msg, hashlib.sha1).digest()

    offset = h[-1] & 0x0F
    truncated = struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF

    code = truncated % 1000000
    return f"{code:06d}"

def verify_totp(hex_seed: str, code: str) -> bool:
    now = int(time.time())
    for offset in [-30, 0, 30]:
        if generate_totp(hex_seed, now + offset) == code:
            return True
    return False
