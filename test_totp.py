from app.scripts.totp_utils import generate_totp
import time

seed = "10e8cefe8e69569c7c1527688fb5c2f49af448d8ab8b85053533bc8f6fbf3b23"

while True:
    print(generate_totp(seed))
    time.sleep(1)
