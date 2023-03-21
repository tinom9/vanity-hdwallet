ETH, BTC, ATOM = "ETH", "BTC", "ATOM"

CURRENCIES = [ETH, BTC, ATOM]

CURRENCY_REGEX_MAP = {
    ETH: r"^[0-9a-fA-F]{,40}$",
    BTC: r"^[02-9ac-hj-np-z]{,38}$",
    ATOM: r"^[02-9ac-hj-np-z]{,37}$",
}

CURRENCY_OPTIONS_MAP = {ETH: (22, 16), BTC: (34, 34), ATOM: (34, 34)}

CURRENCY_PREFIX_MAP = {ETH: "0x", BTC: "bc1q", ATOM: "cosmos1"}

CURRENCY_PATH_MAP = {
    ETH: "m/44'/60'/0'/0/0",
    BTC: "m/84'/0'/0'/0/0",
    ATOM: "m/44'/118'/0'/0/0",
}
