import hashlib

def hash_sha256(string):
    encoded = string.encode()
    result = hashlib.sha256(encoded)
    return result.hexdigest()