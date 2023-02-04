import argparse
import re
import time

from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH
from hdwallet.utils import generate_mnemonic

parser = argparse.ArgumentParser()
parser.add_argument("--vanity", type=str)
parser.add_argument("--currency", type=str, default=ETH)
parser.add_argument("--case-sensitive", type=bool, default=False)
args = parser.parse_args()

vanity = args.vanity
currency = args.currency.upper()
case_sensitive = args.case_sensitive

CURRENCY_REGEX_MAP = {ETH: r"^[0-9a-fA-F]{,40}$", BTC: r"^[0-9a-hj-np-z]{,38}$"}

CURRENCY_OPTIONS_MAP = {ETH: (22, 16), BTC: (34, 34)}

CURRENCY_ADDRESS_MAP = {ETH: "p2pkh", BTC: "p2wpkh"}

CURRENCY_PREFIX_MAP = {ETH: "0x", BTC: "bc1q"}


def check_vanity_validity(currency: str, vanity: str) -> bool:
    return bool(re.match(CURRENCY_REGEX_MAP[currency], vanity))


def calculate_estimated_tries(currency: str, vanity: str, case_sensitive: bool) -> int:
    max_options, min_options = CURRENCY_OPTIONS_MAP[currency]
    options = max_options if case_sensitive else min_options
    return options ** len(vanity)


def calculate_estimated_time(estimated_tries: int, tries: int, time_elapsed: float):
    return estimated_tries * time_elapsed / tries if tries else 0


def generate_hd_wallet(hdwallet: HDWallet) -> tuple[str, dict]:
    mnemonic = generate_mnemonic()
    hdwallet.clean_derivation()
    hdwallet.from_mnemonic(mnemonic=mnemonic)
    return (mnemonic, hdwallet.dumps())


def check_wallet_vanity(wallet: dict, vanity: str, case_sensitive: bool) -> bool:
    address = wallet["addresses"][CURRENCY_ADDRESS_MAP[wallet["symbol"]]]
    prefix = CURRENCY_PREFIX_MAP[wallet["symbol"]]
    generated = address[len(prefix) : len(vanity) + len(prefix)]
    if case_sensitive:
        return generated == vanity
    else:
        return generated.lower() == vanity.lower()


def generate_vanity_wallet(vanity: str, case_sensitive: bool) -> None:
    print("Generating vanity wallet\n\n\n\n")
    found = False
    count = 0
    hdwallet = HDWallet(symbol=currency, use_default_path=True)
    start_time = time.time()
    estimated_tries = calculate_estimated_tries(currency, vanity, case_sensitive)
    while not found:
        count += 1
        time_elapsed = time.time() - start_time
        estimated_time = calculate_estimated_time(
            estimated_tries, count - 1, time_elapsed
        )
        print(
            (
                "\x1B[4A"
                f" · Tries: {count}\n"
                f" · Estimated tries (50% probability): {estimated_tries}\n"
                f" · Time elapsed: {'%.2f'%(time_elapsed)} s\n"
                f" · Estimated time (50% probability): {'%.2f'%(estimated_time)} s"
            ),
            end="\n",
            flush=True,
        )
        mnemonic, wallet = generate_hd_wallet(hdwallet)
        if check_wallet_vanity(wallet, vanity, case_sensitive):
            found = True
            print("Vanity address generated!")
            print(mnemonic)
            print(wallet["addresses"][CURRENCY_ADDRESS_MAP[wallet["symbol"]]])


if __name__ == "__main__":
    if not currency in [ETH, BTC]:
        raise Exception(
            f"{currency} is not a valid currency. Supported currencies are: {ETH}, {BTC}."
        )
    if not check_vanity_validity(currency, vanity):
        raise Exception(f"{vanity} is not a valid vanity.")
    generate_vanity_wallet(vanity, case_sensitive)
