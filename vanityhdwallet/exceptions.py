from vanityhdwallet.currencies import CURRENCIES


class InvalidCurrencyException(Exception):
    def __init__(self, currency: str):
        super().__init__(
            f"{currency} is not a valid currency. Supported currencies are: "
            f"{', '.join(CURRENCIES)}."
        )


class InvalidVanityException(Exception):
    def __init__(self, vanity: str, currency: str):
        super().__init__(f"{vanity} is not a valid {currency} vanity.")
