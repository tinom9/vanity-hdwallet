import hashlib

from Crypto.Hash import RIPEMD160, keccak


def keccak256(b: bytes) -> bytes:
    h = keccak.new(data=b, digest_bits=256)
    return h.digest()


def ripemd160(b: bytes) -> bytes:
    r = RIPEMD160.new(data=b)
    return r.digest()


def sha3(b: bytes) -> bytes:
    s = hashlib.new("sha256", b)
    return s.digest()
