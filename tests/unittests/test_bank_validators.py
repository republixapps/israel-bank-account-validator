import json
import os

import allure
import pytest

from israel_bank_account_validator import BANK_VALIDATORS
from israel_bank_account_validator import number_digits_to_list
from israel_bank_account_validator import SUPPORTED_BANKS


def load_data():
    file_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'test_bank_validators_data.json')
    with open(file_) as f:
        data = json.load(f)

    test_cases = []
    for name, cases in data.items():
        for case in cases:
            test_cases.append((name, *case.values()))
    return test_cases


TEST_DATA = load_data()


@allure.feature("Bank account validation")
@allure.story("Validate bank account")
@allure.title("Test bank account validation")
@allure.description("Check bank account validation")
@pytest.mark.parametrize("bank_name, bank_number, account_number, branch_number, account_length, expected", TEST_DATA)
def test_bank_validators(bank_name, bank_number, account_number, branch_number, account_length, expected):
    bank_validator = BANK_VALIDATORS[SUPPORTED_BANKS[bank_name]]

    with allure.step(f"Validate bank account for {bank_name}"):
        validated = bank_validator(
            branch_number,
            number_digits_to_list(account_number, account_length),
            number_digits_to_list(branch_number, 3)
        )
        assert validated == expected
