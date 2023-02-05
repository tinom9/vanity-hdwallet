import argparse
import multiprocessing as mp
import time

from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH

from vanityhdwallet.helpers import (
    calculate_estimated_time,
    calculate_estimated_tries,
    check_address_vanity,
    check_vanity_validity,
    generate_hd_keypair,
)

parser = argparse.ArgumentParser()
parser.add_argument("--vanity", type=str)
parser.add_argument("--currency", type=str, default=ETH)
parser.add_argument("--case-sensitive", type=bool, default=False)
args = parser.parse_args()

vanity = args.vanity
currency = args.currency.upper()
case_sensitive = args.case_sensitive


def generate_vanity_wallet(vanity: str, case_sensitive: bool) -> None:
    print("Generating vanity wallet\n\n\n\n")
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
        with mp.Pool(processes=N) as p:
            wallets = p.map(generate_hd_keypair, [hdwallet] * N)
        for mnemonic, address in wallets:
            if check_address_vanity(currency, address, vanity, case_sensitive):
                found = True
                print("Vanity address generated!")
                print(mnemonic)
                print(address)


if __name__ == "__main__":
    if not currency in [ETH, BTC]:
        raise Exception(
            f"{currency} is not a valid currency. Supported currencies are: {ETH}, {BTC}."
        )
    if not check_vanity_validity(currency, vanity):
        raise Exception(f"{vanity} is not a valid vanity.")
    generate_vanity_wallet(vanity, case_sensitive)
