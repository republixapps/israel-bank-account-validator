import json

import allure
import pytest

from israel_bank_account_validator import BANK_VALIDATORS
from israel_bank_account_validator import number_digits_to_list
from israel_bank_account_validator import SUPPORTED_BANKS

# Load test data from JSON file
with open('data/test_bank_validators_data.json') as f:
    test_data = json.load(f)

# Flatten the test data to create a single list of test cases
test_cases = []
for name, cases in test_data.items():
    for case in cases:
        test_cases.append((name, *case.values()))


@allure.feature("Bank account validation")
@allure.story("Validate bank account")
@allure.title("Test bank account validation")
@allure.description("Check bank account validation")
@pytest.mark.parametrize("bank_name, bank_number, account_number, branch_number, account_length, expected", test_cases)
def test_bank_validators(bank_name, bank_number, account_number, branch_number, account_length, expected):
    bank_validator = BANK_VALIDATORS[SUPPORTED_BANKS[bank_name]]
    assert bank_validator(bank_number, number_digits_to_list(account_number, account_length),
                          number_digits_to_list(branch_number, 3)) == expected
