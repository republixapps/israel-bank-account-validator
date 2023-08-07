import unittest

from israel_bank_account_validator import BankAccountNumberValueError
from israel_bank_account_validator import BankBranchNumberValueError
from israel_bank_account_validator import BankNumberValueError
from israel_bank_account_validator import UnsupportedBankError
from israel_bank_account_validator import validate_bank_account


class TestBankAccountValidation(unittest.TestCase):

    def test_valid_account(self):
        bank_number = '11'  # BANK DISCOUNT
        bank_branch_number = '111'
        account_number = '000032018'
        self.assertTrue(validate_bank_account(bank_number, bank_branch_number, account_number))

    def test_invalid_account(self):
        bank_number = '20'  # BANK MIZRAHI TEFAHOT
        bank_branch_number = '006'
        account_number = '000160779'
        self.assertFalse(validate_bank_account(bank_number, bank_branch_number, account_number))

    def test_empty_values(self):
        bank_number = ''
        bank_branch_number = '006'
        account_number = '000160779'

        with self.assertRaises(BankNumberValueError):
            validate_bank_account(bank_number, bank_branch_number, account_number)

        bank_number = '11'
        bank_branch_number = ''
        with self.assertRaises(BankBranchNumberValueError):
            validate_bank_account(bank_number, bank_branch_number, account_number)

        bank_branch_number = '006'
        account_number = ''
        with self.assertRaises(BankAccountNumberValueError):
            self.assertFalse(validate_bank_account(bank_number, bank_branch_number, account_number))

    def test_non_string_input(self):
        bank_number = 11
        bank_branch_number = 111
        account_number = 1111111
        self.assertFalse(validate_bank_account(bank_number, bank_branch_number, account_number))

    def test_unsupported_bank(self):
        bank_number = '99999999999'
        bank_branch_number = '006'
        account_number = '000160779'
        with self.assertRaises(UnsupportedBankError):
            validate_bank_account(bank_number, bank_branch_number, account_number)

    def test_negative_bank_number(self):
        bank_number = '-1'
        bank_branch_number = '006'
        account_number = '000160779'
        with self.assertRaises(BankNumberValueError):
            validate_bank_account(bank_number, bank_branch_number, account_number)

    def test_negative_bank_branch_number(self):
        bank_number = '11'
        bank_branch_number = '-6'
        account_number = '000160779'
        with self.assertRaises(BankBranchNumberValueError):
            validate_bank_account(bank_number, bank_branch_number, account_number)

    def test_negative_account_number(self):
        bank_number = '11'
        bank_branch_number = '006'
        account_number = '-000160779'
        with self.assertRaises(BankAccountNumberValueError):
            validate_bank_account(bank_number, bank_branch_number, account_number)


if __name__ == '__main__':
    unittest.main()
