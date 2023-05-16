import hashlib
import hmac

import coincurve

PBKDF2_ROUNDS = 2048
HARDENED_INDEX = 0x80000000


def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    """Takes a mnemonic and a passphrase and returns a 64 bytes seed."""
    passphrase = "mnemonic" + passphrase
    mnemonic_bytes = mnemonic.encode("utf-8")
    passphrase_bytes = passphrase.encode("utf-8")
    stretched = hashlib.pbkdf2_hmac(
        "sha512", mnemonic_bytes, passphrase_bytes, PBKDF2_ROUNDS
    )
    return stretched[:64]


def derive_private_key_from_seed(seed: bytes) -> tuple[bytes, bytes]:
    """Takes a 64 bytes seed and returns a 32 bytes privkey and a 32 bytes chaincode."""
    secret = hmac.new("Bitcoin seed".encode(), seed, hashlib.sha512).digest()
    privkey, chaincode = secret[:32], secret[32:]
    return privkey, chaincode


def privkey_to_pubkey(privkey: bytes) -> bytes:
    """Takes a 32 bytes privkey and returns a 33 bytes secp256k1 pubkey."""
    return coincurve.PublicKey.from_secret(privkey).format()


def get_path_list(path: str) -> list[int]:
    """Takes a path and returns a list of indexes."""
    indexes = path.split("/")[1:]
    path_list = []
    for i in indexes:
        if i[-1:] in ["'", "h", "H"]:
            path_list.append(int(i[:-1]) + HARDENED_INDEX)
        else:
            path_list.append(int(i))
    return path_list


def derive_private_child(
    pubkey: bytes, privkey: bytes, chaincode: bytes, index: int, hardened: int
) -> tuple[bytes, bytes]:
    """
    Takes a pubkey, a privkey, a chaincode, an index and a hardened flag and returns a
    32 bytes privkey and a 32 bytes chaincode.
    """
    key = (b"\x00" + privkey) if hardened else pubkey
    payload = hmac.new(
        chaincode, key + index.to_bytes(4, "big"), hashlib.sha512
    ).digest()
    child_private = coincurve.PrivateKey(payload[:32]).add(privkey)
    return child_private.secret, payload[32:]


def derive_public_key(mnemonic: str, path: str) -> bytes:
    """Takes a mnemonic and a path and returns a 33 bytes secp256k1 pubkey."""
    seed = mnemonic_to_seed(mnemonic)
    privkey, chaincode = derive_private_key_from_seed(seed)
    pubkey = privkey_to_pubkey(privkey)
    path_list = get_path_list(path)
    for index in path_list:
        hardened = index & HARDENED_INDEX
        privkey, chaincode = derive_private_child(
            pubkey, privkey, chaincode, index, hardened
        )
        pubkey = privkey_to_pubkey(privkey)
    return pubkey
