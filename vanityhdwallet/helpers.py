import re

from hdwallet import HDWallet
from hdwallet.utils import generate_mnemonic

from vanityhdwallet.currencies import (
    CURRENCY_ADDRESS_MAP,
    CURRENCY_OPTIONS_MAP,
    CURRENCY_PREFIX_MAP,
    CURRENCY_REGEX_MAP,
)


def check_vanity_validity(currency: str, vanity: str) -> bool:
    return bool(re.match(CURRENCY_REGEX_MAP[currency], vanity))


def calculate_estimated_tries(currency: str, vanity: str, case_sensitive: bool) -> int:
    max_options, min_options = CURRENCY_OPTIONS_MAP[currency]
    options = max_options if case_sensitive else min_options
    return options ** len(vanity)


def calculate_estimated_time(estimated_tries: int, tries: int, time_elapsed: float):
    return estimated_tries * time_elapsed / tries if tries else 0


def generate_hd_wallet(hdwallet: HDWallet) -> dict:
    mnemonic = generate_mnemonic()
    hdwallet.clean_derivation()
    hdwallet.from_mnemonic(mnemonic=mnemonic)
    return hdwallet.dumps()


def check_wallet_vanity(wallet: dict, vanity: str, case_sensitive: bool) -> bool:
    address = wallet["addresses"][CURRENCY_ADDRESS_MAP[wallet["symbol"]]]
    prefix = CURRENCY_PREFIX_MAP[wallet["symbol"]]
    generated = address[len(prefix) : len(vanity) + len(prefix)]
    if case_sensitive:
        return generated == vanity
    else:
        return generated.lower() == vanity.lower()
