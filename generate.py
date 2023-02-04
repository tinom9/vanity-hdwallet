from hdwallet import HDWallet
from hdwallet.utils import generate_mnemonic
from hdwallet.symbols import ETH
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--vanity", type=str)
parser.add_argument("--case-sensitive", type=bool, default=False)
args = parser.parse_args()

vanity = args.vanity
case_sensitive = args.case_sensitive

hdwallet = HDWallet(symbol=ETH, use_default_path=True)

def calculate_estimated_tries(vanity: str, case_sensitive: bool) -> int:
    options = 22 if case_sensitive else 16
    return options ** len(vanity)

def calculate_estimated_time(estimated_tries: int, tries: int, time_elapsed: int):
    return estimated_tries * time_elapsed / tries if tries else 0

def generate_hd_wallet() -> tuple[str, dict]:
    mnemonic = generate_mnemonic()
    hdwallet.clean_derivation()
    hdwallet.from_mnemonic(mnemonic=mnemonic)
    return (mnemonic, hdwallet.dumps())

def check_wallet_vanity(wallet: dict, vanity: str) -> bool:
    return wallet["addresses"]["p2pkh"][2:len(vanity)+2] == vanity

def generate_vanity_wallet(vanity: str, case_sensitive: bool) -> None:
    print("Generating vanity wallet\n\n\n\n")
    found = False
    count = 0
    start_time = time.time()
    estimated_tries = calculate_estimated_tries(vanity, case_sensitive)
    while not found:
        count += 1
        time_elapsed = time.time() - start_time
        estimated_time = calculate_estimated_time(estimated_tries, count - 1, time_elapsed)
        print(
            (
            "\x1B[4A"
            f" · Tries: {count}\n"
            f" · Estimated tries (50% probability): {estimated_tries}\n"
            f" · Time elapsed: {'%.2f'%(time_elapsed)} s\n"
            f" · Estimated time (50% probability): {'%.2f'%(estimated_time)} s"
            ),
            end="\n",
            flush=True
        )
        mnemonic, wallet = generate_hd_wallet()
        if check_wallet_vanity(wallet, vanity):
            found = True
            print("Vanity address generated!")
            print(mnemonic)
            print(wallet["addresses"]["p2pkh"])

if __name__ == "__main__":
    generate_vanity_wallet(vanity, case_sensitive)
