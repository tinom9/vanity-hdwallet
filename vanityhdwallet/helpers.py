import multiprocessing as mp
import re
import time
from functools import reduce
from threading import Event

from hdwallet import HDWallet
from hdwallet.utils import generate_mnemonic
from humanfriendly import format_timespan

from vanityhdwallet.currencies import (
    CURRENCY_ADDRESS_MAP,
    CURRENCY_OPTIONS_MAP,
    CURRENCY_PREFIX_MAP,
    CURRENCY_REGEX_MAP,
)
from vanityhdwallet.messages import (
    GENERATING_MESSAGE,
    PROGRESS_MESSAGE,
    WALLET_GENERATED_MESSAGE,
)


def check_vanity_validity(currency: str, vanity: str) -> bool:
    return bool(re.match(CURRENCY_REGEX_MAP[currency], vanity))


def calculate_estimated_tries(currency: str, vanity: str, case_sensitive: bool) -> int:
    max_options, min_options = CURRENCY_OPTIONS_MAP[currency]
    options = max_options if case_sensitive else min_options
    return options ** len(vanity)


def calculate_estimated_time(estimated_tries: int, tries: int, time_elapsed: float):
    return estimated_tries * time_elapsed / tries if tries else 0


def derive_address(hdwallet: HDWallet, mnemonic: str) -> str:
    hdwallet.clean_derivation()
    hdwallet.from_mnemonic(mnemonic=mnemonic)
    wallet = hdwallet.dumps()
    address = wallet["addresses"][CURRENCY_ADDRESS_MAP[wallet["symbol"]]]
    return address


def check_address_vanity(
    currency: str, address: str, vanity: str, case_sensitive: bool
) -> bool:
    prefix = CURRENCY_PREFIX_MAP[currency]
    generated = address[len(prefix) : len(vanity) + len(prefix)]
    if case_sensitive:
        return generated == vanity
    else:
        return generated.lower() == vanity.lower()


def find_vanity_wallet(
    currencies: list[str],
    vanities: list[str],
    case_sensitive: bool,
    active: Event,
    singer: bool,
) -> tuple[str, list[str]] | None:
    hdwallets = [
        HDWallet(symbol=currency, use_default_path=True) for currency in currencies
    ]
    if singer:
        count = 0
        N = mp.cpu_count()
        estimated_tries = reduce(
            (lambda x, y: x * y),
            [
                calculate_estimated_tries(currencies[i], vanities[i], case_sensitive)
                for i in range(len(currencies))
            ],
        )
        start_time = time.time()
    while active.is_set():
        if singer:
            count += N
            time_elapsed = time.time() - start_time
            estimated_time = calculate_estimated_time(
                estimated_tries, count - 1, time_elapsed
            )
            print(
                PROGRESS_MESSAGE.format(
                    count,
                    estimated_tries,
                    format_timespan(int(time_elapsed)),
                    format_timespan(int(estimated_time)),
                ),
                end="",
                flush=True,
            )
        mnemonic = generate_mnemonic()
        addresses = []
        for i, hdwallet in enumerate(hdwallets):
            address = derive_address(hdwallet, mnemonic)
            if check_address_vanity(
                currencies[i], address, vanities[i], case_sensitive
            ):
                addresses.append(address)
            else:
                break
        if len(addresses) == len(hdwallets):
            active.clear()
            return mnemonic, addresses
    return None


def generate_vanity_wallet(currency: str, vanity: str, case_sensitive: bool) -> None:
    print(GENERATING_MESSAGE)
    N = mp.cpu_count()
    with mp.Pool(processes=N) as p:
        manager = mp.Manager()
        active = manager.Event()
        active.set()
        wallets = p.starmap(
            find_vanity_wallet,
            [([currency], [vanity], case_sensitive, active, True)]
            + [([currency], [vanity], case_sensitive, active, False)] * (N - 1),
        )
    mnemonic, addresses = next(wallet for wallet in wallets if wallet)
    print(WALLET_GENERATED_MESSAGE.format(currency, mnemonic, addresses[0]))


def generate_multi_vanity_wallet(
    currencies: list[str], vanities: list[str], case_sensitive: bool
) -> None:
    print(GENERATING_MESSAGE)
    N = mp.cpu_count()
    with mp.Pool(processes=N) as p:
        manager = mp.Manager()
        active = manager.Event()
        active.set()
        wallets = p.starmap(
            find_vanity_wallet,
            [(currencies, vanities, case_sensitive, active, True)]
            + [(currencies, vanities, case_sensitive, active, False)] * (N - 1),
        )
    mnemonic, addresses = next(wallet for wallet in wallets if wallet)
    print(
        WALLET_GENERATED_MESSAGE.format(
            ", ".join(currencies),
            mnemonic,
            "".join(
                [
                    (
                        currencies[i]
                        + ": "
                        + addresses[i]
                        + ("\n" if i < len(currencies) - 1 else "")
                    )
                    for i in range(len(currencies))
                ]
            ),
        )
    )
