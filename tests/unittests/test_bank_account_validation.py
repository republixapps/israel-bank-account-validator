import unittest
from israel_bank_account_validator import validate_bank_account


class TestBankAccountValidation(unittest.TestCase):

    def test_valid_account(self):
        bank_code = "11"  # BANK DISCOUNT
        branch_code = "111"
        account_number = "000032018"
        self.assertTrue(validate_bank_account(bank_code, branch_code, account_number))

    def test_invalid_account(self):
        bank_code = "20"  # BANK MIZRAHI TEFAHOT
        branch_code = "006"
        account_number = "000160779"
        self.assertFalse(validate_bank_account(bank_code, branch_code, account_number))

    def test_empty_values(self):
        bank_code = ""
        branch_code = ""
        account_number = ""
        self.assertFalse(validate_bank_account(bank_code, branch_code, account_number))

    def test_non_string_input(self):
        bank_code = 11
        branch_code = 111
        account_number = 1111111
        self.assertFalse(validate_bank_account(bank_code, branch_code, account_number))

    def test_unsupported_bank(self):
        bank_code = "99999999999"
        branch_code = "006"
        account_number = "000160779"
        self.assertFalse(validate_bank_account(bank_code, branch_code, account_number))

    def test_negative_values(self):
        bank_code = "11"
        branch_code = "-6"
        account_number = "000160779"
        self.assertFalse(validate_bank_account(bank_code, branch_code, account_number))



if __name__ == '__main__':
    unittest.main()
