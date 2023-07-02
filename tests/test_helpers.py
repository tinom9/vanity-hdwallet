import pytest

from vanityhdwallet.currencies import ATOM, BTC, ETH
from vanityhdwallet.helpers import (
    calculate_estimated_time,
    calculate_estimated_tries,
    check_address_vanity,
    check_vanity_validity,
)


@pytest.mark.parametrize(
    # Inputs: currency, vanity.
    # Output: validity.
    ["inputs", "output"],
    [
        # Hexadecimal is valid.
        [[ETH, "abc1234"], True],
        # Case-sensitive hexadecimal is valid.
        [[ETH, "aBc1234"], True],
        # Non-hexadecimal is invalid.
        [[ETH, "abcdefg"], False],
        # Over maximum length is invalid.
        [[ETH, "a" * 42], False],
        # Allowed characters is valid.
        [[BTC, "ac234"], True],
        # Uppercase allowed characters is invalid.
        [[BTC, "AC234"], False],
        # Non-allowed characters is invalid.
        [[BTC, "1"], False],
        [[BTC, "b"], False],
        [[BTC, "i"], False],
        [[BTC, "o"], False],
    ],
)
def test_check_vanity_validity(inputs, output):
    assert output == check_vanity_validity(*inputs)


@pytest.mark.parametrize(
    # Inputs: currency, vanity, case_sensitive.
    # Output: estimated_tries.
    ["inputs", "output"],
    [
        [[ETH, "abc1234", False], 186065279],
        [[ETH, "abc1234", True], 1488522235],
        [[BTC, "abc1234", False], 54318033479],
        [[BTC, "abc1234", True], 54318033479],
        [[ATOM, "abc1234", False], 54318033479],
        [[ATOM, "abc1234", True], 54318033479],
    ],
)
def test_calculate_estimated_tries(inputs, output):
    assert output == calculate_estimated_tries(*inputs)


@pytest.mark.parametrize(
    # Inputs: estimated_tries, tries, time_elapsed.
    # Output: estimated_time.
    ["inputs", "output"],
    [
        # Returns valid value.
        [[10, 5, 2.5], 5],
        # Zero tries returns 0.
        [[10, 0, 0.1], 0],
    ],
)
def test_calculate_estimated_time(inputs, output):
    assert output == calculate_estimated_time(*inputs)


@pytest.mark.parametrize(
    ["currency", "address", "vanity", "case_sensitive", "output"],
    [
        # ETH validations, has case-sensitivity.
        [ETH, "0xcA829FDE4C09390d0a568a9110B26F2513765E66", "ca", False, True],
        [ETH, "0xcA829FDE4C09390d0a568a9110B26F2513765E66", "cb", False, False],
        [ETH, "0xcA829FDE4C09390d0a568a9110B26F2513765E66", "cA", True, True],
        [ETH, "0xcA829FDE4C09390d0a568a9110B26F2513765E66", "ca", True, False],
        # BTC validations, doesn't have case-sensitivity.
        [BTC, "bc1qcaqlu66crud4ulgymhq83q64zacdnxkkm3g86y", "ca", False, True],
        [BTC, "bc1qcaqlu66crud4ulgymhq83q64zacdnxkkm3g86y", "cb", False, False],
        [BTC, "bc1qcaqlu66crud4ulgymhq83q64zacdnxkkm3g86y", "ca", True, True],
    ],
)
def test_check_address_vanity(currency, address, vanity, case_sensitive, output):
    assert output == check_address_vanity(currency, address, vanity, case_sensitive)
