from hashlib import sha256, sha1

def do_sha1(_str):
    return sha1(_str.encode('utf-8')).hexdigest()

def do_sha256(_str):
    return sha256(_str.encode('utf-8')).hexdigest()


