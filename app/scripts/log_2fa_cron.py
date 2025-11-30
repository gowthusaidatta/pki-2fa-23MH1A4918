import os
import time
from scripts.totp_utils import generate_totp

SEED_PATH = "/data/seed.txt"
OUTPUT_PATH = "/cron/last_code.txt"

def load_seed():
    if not os.path.exists(SEED_PATH):
        return None
    with open(SEED_PATH, "r") as f:
        return f.read().strip()

if __name__ == "__main__":
    seed = load_seed()
    if seed is None:
        exit(0)

    code, _ = generate_totp(seed)  # <- FIXED: unpack tuple

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {code}\n"

    with open(OUTPUT_PATH, "a") as f:
        f.write(line)
