# app/scripts/totp_utils.py
import base64
import time
import pyotp

def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-char hex string to base32 (RFC-compatible).
    """
    raw = bytes.fromhex(hex_seed)
    b32 = base64.b32encode(raw).decode("utf-8")
    # pyotp accepts base32 with or without padding; keep default padding
    return b32

def generate_totp(hex_seed: str, interval: int = 30, digits: int = 6):
    """
    Returns tuple: (code_str, valid_for_seconds)
    """
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=digits, interval=interval, digest='sha1')
    code = totp.now()
    # seconds left in period
    epoch = int(time.time())
    valid_for = interval - (epoch % interval)
    return code, valid_for

def verify_totp(hex_seed: str, code: str, valid_window: int = 1, interval: int = 30, digits: int = 6) -> bool:
    """
    Verify using ±valid_window periods (default 1).
    """
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=digits, interval=interval, digest='sha1')
    # pyotp verify accepts valid_window param
    try:
        return totp.verify(code, valid_window=valid_window)
    except Exception:
        return False

if __name__ == "__main__":
    # quick local test (if seed.txt present)
    try:
        with open("seed.txt") as f:
            seed = f.read().strip()
        code, remaining = generate_totp(seed)
        print("Current TOTP code:", code)
        print("Valid for:", remaining, "seconds")
    except FileNotFoundError:
        print("seed.txt not found")
