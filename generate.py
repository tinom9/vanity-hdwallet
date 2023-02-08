import argparse
import multiprocessing as mp
import time

from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH

from vanityhdwallet.exceptions import InvalidCurrencyException, InvalidVanityException
from vanityhdwallet.helpers import (
    calculate_estimated_time,
    calculate_estimated_tries,
    check_address_vanity,
    check_vanity_validity,
    generate_hd_keypair,
)
from vanityhdwallet.messages import (
    ADDRESS_GENERATED_MESSAGE,
    GENERATING_MESSAGE,
    PROGRESS_MESSAGE,
)

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vanity", type=str)
parser.add_argument("-c", "--currency", type=str, default=ETH)
parser.add_argument("--case-sensitive", action="store_true")
args = parser.parse_args()

vanity = args.vanity
currency = args.currency.upper()
case_sensitive = args.case_sensitive


def generate_vanity_wallet(vanity: str, case_sensitive: bool) -> None:
    print(GENERATING_MESSAGE)
    found = False
    count = 0
    N = mp.cpu_count()
    hdwallet = HDWallet(symbol=currency, use_default_path=True)
    start_time = time.time()
    estimated_tries = calculate_estimated_tries(currency, vanity, case_sensitive)
    while not found:
        count += N
        time_elapsed = time.time() - start_time
        estimated_time = calculate_estimated_time(
            estimated_tries, count - 1, time_elapsed
        )
        print(
            PROGRESS_MESSAGE.format(
                count, estimated_tries, time_elapsed, estimated_time
            ),
            end="\n",
            flush=True,
        )
        with mp.Pool(processes=N) as p:
            wallets = p.map(generate_hd_keypair, [hdwallet] * N)
        for mnemonic, address in wallets:
            if check_address_vanity(currency, address, vanity, case_sensitive):
                found = True
                print(ADDRESS_GENERATED_MESSAGE.format(currency, mnemonic, address))


if __name__ == "__main__":
    if not currency in [ETH, BTC]:
        raise InvalidCurrencyException(currency)
    if not check_vanity_validity(currency, vanity):
        raise InvalidVanityException(vanity, currency)
    generate_vanity_wallet(vanity, case_sensitive)
