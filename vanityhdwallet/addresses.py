import bech32
from coincurve import PublicKey

from vanityhdwallet.cryptography import keccak256, ripemd160, sha3
from vanityhdwallet.currencies import ATOM, BTC, CURRENCY_PATH_MAP, ETH
from vanityhdwallet.derivations import derive_public_key


def to_checksum_address(address: str) -> str:
    address_hash = keccak256(address.encode()).hex()
    chars = []
    for a, h in zip(address, address_hash):
        if int(h, 16) >= 8:
            chars.append(a.upper())
        else:
            chars.append(a)
    return "0x" + "".join(chars)


def get_bech32_address(pk: bytes, hrp: str, version: int | None = None) -> str:
    s = sha3(pk)
    r = ripemd160(s)
    five_bit_r: list[int] = bech32.convertbits(r, 8, 5)  # type: ignore[assignment]
    data = [version] + five_bit_r if version is not None else five_bit_r
    return bech32.bech32_encode(hrp, data)


def get_ethereum_address(mnemonic: str) -> str:
    pk = derive_public_key(mnemonic, CURRENCY_PATH_MAP[ETH])
    pk = PublicKey(pk).format(False)[1:]
    return to_checksum_address(f"{keccak256(pk)[-20:].hex()}")


def get_bitcoin_address(mnemonic: str) -> str:
    pk = derive_public_key(mnemonic, CURRENCY_PATH_MAP[BTC])
    return get_bech32_address(pk, "bc", 0)


def get_cosmos_address(mnemonic: str) -> str:
    pk = derive_public_key(mnemonic, CURRENCY_PATH_MAP[ATOM])
    return get_bech32_address(pk, "cosmos")


CURRENCY_ADDRESS_FUNCTION_MAP = {
    ETH: get_ethereum_address,
    BTC: get_bitcoin_address,
    ATOM: get_cosmos_address,
}


def get_currency_address(currency: str, mnemonic: str) -> str:
    return CURRENCY_ADDRESS_FUNCTION_MAP[currency](mnemonic)
