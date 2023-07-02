from vanityhdwallet.currencies import CURRENCIES, LANGUAGES, PHRASE_LENGHTS


class InvalidCurrencyException(Exception):
    def __init__(self, currency: str):
        super().__init__(
            f"{currency} is not a valid currency. Supported currencies are: "
            f"{', '.join(CURRENCIES)}."
        )


class InvalidVanityException(Exception):
    def __init__(self, vanity: str, currency: str):
        super().__init__(f"{vanity} is not a valid {currency} vanity.")


class InvalidLanguageException(Exception):
    def __init__(self, language: str):
        super().__init__(
            f"{language} is not a valid language. Supported languages are: "
            f"{', '.join(LANGUAGES)}."
        )


class InvalidPhraseLengthException(Exception):
    def __init__(self, length: int):
        super().__init__(
            f"{length} is not a valid phrase length. Supported lengths are: "
            f"{', '.join([str(length) for length in PHRASE_LENGHTS])}."
        )
