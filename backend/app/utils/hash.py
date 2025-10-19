import hashlib


def create_text_hash(txt: str):
    encoded_txt = txt.encode('utf-8')
    hash_obj = hashlib.sha256(encoded_txt)
    hex_digest = hash_obj.hexdigest()
    return hex_digest