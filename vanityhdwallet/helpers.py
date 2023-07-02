import math
import multiprocessing as mp
import re
import time
from functools import reduce
from threading import Event

from humanfriendly import format_timespan
from mnemonic import Mnemonic

from vanityhdwallet.addresses import get_currency_address
from vanityhdwallet.currencies import (
    CHECKSUMMABLE_CURRENCIES,
    CURRENCY_OPTIONS_MAP,
    CURRENCY_PREFIX_MAP,
    CURRENCY_REGEX_MAP,
)
from vanityhdwallet.messages import (
    GENERATING_MESSAGE,
    PROGRESS_MESSAGE,
    WALLET_GENERATED_MESSAGE,
)


def generate_mnemonic(language: str = "english", strength: int = 128) -> str:
    return Mnemonic(language=language).generate(strength=strength)


def check_vanity_validity(currency: str, vanity: str) -> bool:
    return bool(re.match(CURRENCY_REGEX_MAP[currency], vanity))


def calculate_difficulty(currency: str, vanity: str, case_sensitive: bool) -> int:
    options = CURRENCY_OPTIONS_MAP[currency]
    difficulty = options ** len(vanity)
    if case_sensitive and currency in CHECKSUMMABLE_CURRENCIES:
        difficulty *= 2 ** sum(c.isalpha() for c in vanity)
    return difficulty


def calculate_estimated_tries(currency: str, vanity: str, case_sensitive: bool) -> int:
    difficulty = calculate_difficulty(currency, vanity, case_sensitive)
    estimated_tries = int(math.log(0.5) / math.log(1 - 1 / difficulty))
    return estimated_tries


def calculate_estimated_time(estimated_tries: int, tries: int, time_elapsed: float):
    return estimated_tries * time_elapsed / tries if tries else 0


def check_address_vanity(
    currency: str, address: str, vanity: str, case_sensitive: bool
) -> bool:
    prefix = CURRENCY_PREFIX_MAP[currency]
    vanity_start = len(prefix)
    vanity_end = len(vanity) + len(prefix)
    generated = address[vanity_start:vanity_end]
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
        for i, currency in enumerate(currencies):
            address = get_currency_address(currency, mnemonic)
            if check_address_vanity(currency, address, vanities[i], case_sensitive):
                addresses.append(address)
            else:
                break
        if len(addresses) == len(currencies):
            active.clear()
            return mnemonic, addresses
    return None


def generate(
    currencies: list[str], vanities: list[str], case_sensitive: bool
) -> tuple[str, list[str]]:
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
    return mnemonic, addresses


def generate_vanity_wallet(currency: str, vanity: str, case_sensitive: bool) -> None:
    print(GENERATING_MESSAGE)
    mnemonic, addresses = generate([currency], [vanity], case_sensitive)
    print(WALLET_GENERATED_MESSAGE.format(currency, mnemonic, addresses[0]))


def generate_multi_vanity_wallet(
    currencies: list[str], vanities: list[str], case_sensitive: bool
) -> None:
    print(GENERATING_MESSAGE)
    mnemonic, addresses = generate(currencies, vanities, case_sensitive)
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
