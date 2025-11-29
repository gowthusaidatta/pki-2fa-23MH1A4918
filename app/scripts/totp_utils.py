import hmac, hashlib, time

def totp(hex_seed, digits=6, interval=30):
    # hex string → bytes
    key = bytes.fromhex(hex_seed)

    counter = int(time.time()) // interval
    msg = counter.to_bytes(8, "big")

    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    code = (int.from_bytes(h[o:o+4], "big") & 0x7fffffff) % (10**digits)

    return str(code).zfill(digits)
