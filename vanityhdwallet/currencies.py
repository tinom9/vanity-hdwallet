ETH, BTC, ATOM = "ETH", "BTC", "ATOM"

CURRENCIES = [ETH, BTC, ATOM]

CHECKSUMMABLE_CURRENCIES = [ETH]

PHRASE_LENGHTS = [12, 15, 18, 21, 24]

(
    ENGLISH,
    SPANISH,
    ITALIAN,
    FRENCH,
    CHINESE_SIMPLIFIED,
    CHINESE_TRADITIONAL,
    JAPANESE,
    KOREAN,
) = (
    "english",
    "spanish",
    "italian",
    "french",
    "chinese_simplified",
    "chinese_traditional",
    "japanese",
    "korean",
)

LANGUAGES = [
    ENGLISH,
    SPANISH,
    ITALIAN,
    FRENCH,
    CHINESE_SIMPLIFIED,
    CHINESE_TRADITIONAL,
    JAPANESE,
    KOREAN,
]

CURRENCY_REGEX_MAP = {
    ETH: r"^[0-9a-fA-F]{,40}$",
    BTC: r"^[02-9ac-hj-np-z]{,38}$",
    ATOM: r"^[02-9ac-hj-np-z]{,37}$",
}

CURRENCY_OPTIONS_MAP = {ETH: 16, BTC: 36, ATOM: 36}

CURRENCY_PREFIX_MAP = {ETH: "0x", BTC: "bc1q", ATOM: "cosmos1"}

CURRENCY_PATH_MAP = {
    ETH: "m/44'/60'/0'/0/0",
    BTC: "m/84'/0'/0'/0/0",
    ATOM: "m/44'/118'/0'/0/0",
}
