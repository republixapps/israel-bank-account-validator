import json

import allure
import pytest

from israel_bank_account_validator import BankAccountNumberValueError
from israel_bank_account_validator import BankBranchNumberValueError
from israel_bank_account_validator import BankNumberValueError
from israel_bank_account_validator import UnsupportedBankError
from israel_bank_account_validator import validate_bank_account

EXCEPTIONS = {
    "BankNumberValueError": BankNumberValueError,
    "BankBranchNumberValueError": BankBranchNumberValueError,
    "BankAccountNumberValueError": BankAccountNumberValueError,
    "UnsupportedBankError": UnsupportedBankError
}


def load_test_data():
    with open('data/test_bank_account_data.json') as f:
        data = json.load(f)
    return data['test_cases']


@allure.story("Validate bank account")
@allure.feature("Bank account validation")
@allure.title("Test bank account validation")
@allure.description("Check bank account validation")
@pytest.mark.parametrize('test_case', load_test_data())
def test_bank_account_validation(test_case):
    bank_number = test_case['bank_number']
    bank_branch_number = test_case['bank_branch_number']
    account_number = test_case['account_number']

    expected_result = test_case.get('expected_result')
    expected_exception = test_case.get('expected_exception')

    if expected_exception:
        with pytest.raises(EXCEPTIONS[expected_exception]):
            validate_bank_account(bank_number, bank_branch_number, account_number)
    else:
        assert validate_bank_account(bank_number, bank_branch_number, account_number) == expected_result
