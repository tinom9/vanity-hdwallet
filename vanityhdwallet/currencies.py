ETH, BTC = "ETH", "BTC"

CURRENCIES = [ETH, BTC]

CURRENCY_REGEX_MAP = {ETH: r"^[0-9a-fA-F]{,40}$", BTC: r"^[02-9ac-hj-np-z]{,38}$"}

CURRENCY_OPTIONS_MAP = {ETH: (22, 16), BTC: (34, 34)}

CURRENCY_PREFIX_MAP = {ETH: "0x", BTC: "bc1q"}

CURRENCY_PATH_MAP = {
    ETH: "m/44'/60'/0'/0/0",
    BTC: "m/84'/0'/0'/0/0",
}

CURRENCY_ADDRESS_MAP = {ETH: "p2pkh", BTC: "p2wpkh"}
