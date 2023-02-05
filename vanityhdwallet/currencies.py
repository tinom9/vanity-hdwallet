from hdwallet.symbols import BTC, ETH

CURRENCY_REGEX_MAP = {ETH: r"^[0-9a-fA-F]{,40}$", BTC: r"^[0-9a-hj-np-z]{,38}$"}

CURRENCY_OPTIONS_MAP = {ETH: (22, 16), BTC: (34, 34)}

CURRENCY_ADDRESS_MAP = {ETH: "p2pkh", BTC: "p2wpkh"}

CURRENCY_PREFIX_MAP = {ETH: "0x", BTC: "bc1q"}
