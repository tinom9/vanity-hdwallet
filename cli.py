import argparse
import sys

from vanityhdwallet.currencies import (
    CURRENCIES,
    ENGLISH,
    ETH,
    LANGUAGES,
    PHRASE_LENGHTS,
)
from vanityhdwallet.exceptions import (
    InvalidCurrencyException,
    InvalidLanguageException,
    InvalidPhraseLengthException,
    InvalidVanityException,
)
from vanityhdwallet.helpers import (
    check_vanity_validity,
    generate_multi_vanity_wallet,
    generate_vanity_wallet,
)


class VanityHDWallet:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command", choices=["generate", "multigenerate"])
        args = parser.parse_args(sys.argv[1:2])
        command = args.command
        getattr(self, command)()

    def generate(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--vanity", type=str)
        parser.add_argument("-c", "--currency", type=str, default=ETH)
        parser.add_argument("-l", "--language", type=str, default=ENGLISH)
        parser.add_argument("-w", "--words", type=int, default=12)
        parser.add_argument("--case-sensitive", action="store_true")
        args = parser.parse_args(sys.argv[2:])
        vanity = args.vanity
        currency = args.currency.upper()
        language = args.language
        words = args.words
        case_sensitive = args.case_sensitive
        if currency not in CURRENCIES:
            raise InvalidCurrencyException(currency)
        if not check_vanity_validity(currency, vanity):
            raise InvalidVanityException(vanity, currency)
        if language not in LANGUAGES:
            raise InvalidLanguageException(language)
        if words not in PHRASE_LENGHTS:
            raise InvalidPhraseLengthException(words)
        generate_vanity_wallet(currency, vanity, language, words, case_sensitive)

    def multigenerate(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--vanities", type=str)
        parser.add_argument("-c", "--currencies", type=str, default=ETH)
        parser.add_argument("-l", "--language", type=str, default=ENGLISH)
        parser.add_argument("-w", "--words", type=int, default=12)
        parser.add_argument("--case-sensitive", action="store_true")
        args = parser.parse_args(sys.argv[2:])
        vanities = args.vanities.split(",")
        currencies = [currency.upper() for currency in args.currencies.split(",")]
        language = args.language
        words = args.words
        case_sensitive = args.case_sensitive
        if invalid_currencies := [
            currency for currency in currencies if currency not in CURRENCIES
        ]:
            raise InvalidCurrencyException(invalid_currencies[0])
        if invalid_vanities_with_currencies := [
            (vanity, currencies[i])
            for i, vanity in enumerate(vanities)
            if not check_vanity_validity(currencies[i], vanity)
        ]:
            invalid_vanities, corresponding_currencies = zip(
                *invalid_vanities_with_currencies
            )
            raise InvalidVanityException(
                invalid_vanities[0], corresponding_currencies[0]
            )
        if language not in LANGUAGES:
            raise InvalidLanguageException(language)
        if words not in PHRASE_LENGHTS:
            raise InvalidPhraseLengthException(words)
        generate_multi_vanity_wallet(
            currencies, vanities, language, words, case_sensitive
        )


if __name__ == "__main__":
    VanityHDWallet()
