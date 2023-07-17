import unittest

from israel_bank_account_validator import BANK_VALIDATORS, SUPPORTED_BANKS, number_digits_to_list


class TestBankValidators(unittest.TestCase):
    def test_yahav_validator(self):
        # Account number: 760050, Branch number: 482, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](482, number_digits_to_list(760050, 6),
                                                                       number_digits_to_list(482, 3)))

        # Account number: 760051, Branch number: 482, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](482, number_digits_to_list(760051, 6),
                                                                        number_digits_to_list(482, 3)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 123456, Branch number: 912, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](912, number_digits_to_list(123456, 6),
                                                                       number_digits_to_list(912, 3)))

        # Assume these made-up data: Account number: 123457, Branch number: 912, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](912, number_digits_to_list(123457, 6),
                                                                        number_digits_to_list(912, 3)))

    def test_post_validator(self):
        # Account number: 9121950, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['POST']](None, number_digits_to_list(9121950, 9)))

        # Account number: 9121951, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['POST']](None, number_digits_to_list(9121951, 9)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 123456789, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['POST']](None, number_digits_to_list(123456789, 9)))

        # Assume these made-up data: Account number: 123456788, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['POST']](None, number_digits_to_list(123456788, 9)))

    def test_leumi_validator(self):
        # Account number: 696870, Branch number: 639, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](639, number_digits_to_list(696870, 8),
                                                                       number_digits_to_list(639, 3)))

        # Account number: 696871, Branch number: 639, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](639, number_digits_to_list(696871, 8),
                                                                        number_digits_to_list(639, 3)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 12345678, Branch number: 912, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](912, number_digits_to_list(12345678, 8),
                                                                       number_digits_to_list(912, 3)))

        # Assume these made-up data: Account number: 12345679, Branch number: 912, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](912, number_digits_to_list(12345679, 8),
                                                                        number_digits_to_list(912, 3)))

    def test_discount_validator(self):
        # Account number: 810230000, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['DISCOUNT']](None, number_digits_to_list(810230000, 9)))

        # Account number: 810230001, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['DISCOUNT']](None, number_digits_to_list(810230001, 9)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 123456789, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['DISCOUNT']](None, number_digits_to_list(123456789, 9)))

        # Assume these made-up data: Account number: 123456788, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['DISCOUNT']](None, number_digits_to_list(123456788, 9)))

    def test_hapoalim_validator(self):
        # Account number: 11140, Branch number: 175, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](175, number_digits_to_list(11140, 5),
                                                                          number_digits_to_list(175, 3)))

        # Account number: 11141, Branch number: 175, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](175, number_digits_to_list(11141, 5),
                                                                           number_digits_to_list(175, 3)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 12345, Branch number: 678, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](678, number_digits_to_list(12345, 5),
                                                                          number_digits_to_list(678, 3)))

        # Assume these made-up data: Account number: 12346, Branch number: 678, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](678, number_digits_to_list(12346, 5),
                                                                           number_digits_to_list(678, 3)))

    def test_igud_validator(self):
        # Account number: 22001711, branch number: 706, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](number_digits_to_list(706, 3),
                                                                      number_digits_to_list(22001711, 8)))

        # Account number: 22001712, branch number: 706, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](number_digits_to_list(706, 3),
                                                                       number_digits_to_list(22001712, 8)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 12345678, branch number: 123, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](number_digits_to_list(123, 3),
                                                                      number_digits_to_list(12345678, 8)))

        # Assume these made-up data: Account number: 12345677, branch number: 123, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](number_digits_to_list(123, 3),
                                                                       number_digits_to_list(12345677, 8)))

    def test_otsar_ahayal_validator(self):
        # Account number: 611140, branch number: 175, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](number_digits_to_list(175, 3),
                                                                               number_digits_to_list(611140, 6)))

        # Account number: 611141, branch number: 175, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](number_digits_to_list(175, 3),
                                                                                number_digits_to_list(611141, 6)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 123456, branch number: 123, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](number_digits_to_list(123, 3),
                                                                               number_digits_to_list(123456, 6)))

        # Assume these made-up data: Account number: 123455, branch number: 123, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](number_digits_to_list(123, 3),
                                                                                number_digits_to_list(123455, 6)))

    def test_one_zero_validator(self):
        # Account number: 1234567, branch number: 1, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](number_digits_to_list(1, 3),
                                                                          number_digits_to_list(1234567, 7)))

        # Account number: 1234568, branch number: 1, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](number_digits_to_list(1, 3),
                                                                           number_digits_to_list(1234568, 7)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 7654321, branch number: 2, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](number_digits_to_list(2, 3),
                                                                          number_digits_to_list(7654321, 7)))

        # Assume these made-up data: Account number: 7654320, branch number: 2, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](number_digits_to_list(2, 3),
                                                                           number_digits_to_list(7654320, 7)))

    def test_mizrahi_validator(self):
        # Account number: 877061, Branch number: 406, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](406, number_digits_to_list(877061, 6),
                                                                         number_digits_to_list(406, 3)))

        # Account number: 877062, Branch number: 406, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](406, number_digits_to_list(877062, 6),
                                                                          number_digits_to_list(406, 3)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 123456, Branch number: 912, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](912, number_digits_to_list(123456, 6),
                                                                         number_digits_to_list(912, 3)))

        # Assume these made-up data: Account number: 123457, Branch number: 912, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](912, number_digits_to_list(123457, 6),
                                                                          number_digits_to_list(912, 3)))

    def test_citybank_validator(self):
        # Account number: 10142007, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['CITYBANK']](number_digits_to_list(10142007, 8)))

        # Account number: 10142008, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['CITYBANK']](number_digits_to_list(10142008, 8)))

        # Additional Test Cases
        # Test with made-up data. You should replace these with real test cases.
        # Assume these made-up data: Account number: 76543212, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['CITYBANK']](number_digits_to_list(76543212, 8)))

        # Assume these made-up data: Account number: 76543210, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['CITYBANK']](number_digits_to_list(76543210, 8)))

    def test_hsbc_validator(self):
        # For branch 101, account number should have 7th digit from the left as 4
        # Account number: 123456789, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](number_digits_to_list(123456789, 9)))

        # Account number: 123456489, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](number_digits_to_list(123456489, 9)))

        # For branch 102, account number should end with 001
        # Account number: 123456001, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](number_digits_to_list(123456001, 9)))

        # Account number: 123456002, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](number_digits_to_list(123456002, 9)))

    def test_beinleumi_validator(self):
        # For Beinleumi, the sum of each digit multiplied by its position (starting from 1)
        # should be divisible by 11 with remainder of 0 or 6.
        # When an account fails this validation, it should validate against the rightmost 6 digits with the same rule.

        # Account number: 8102300008, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](number_digits_to_list(8102300008, 10)))

        # Account number: 8102300007, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](number_digits_to_list(8102300007, 10)))

        # Account number: 10230008, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](number_digits_to_list(10230008, 8)))

        # Account number: 123456 (fails the first test, passes the second test as the rightmost 6 digits are valid)
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](number_digits_to_list(123456, 6)))

        # Account number: 1234567 (fails the first test, fails the second test as the rightmost 6 digits are invalid)
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](number_digits_to_list(1234567, 7)))

    def test_masad_validator(self):
        # For Masad, the sum of each digit multiplied by its position (starting from 1)
        # should be divisible by 11 with no remainder except for specific branch numbers,
        # where remainders of 0 and 2 are also valid.

        # Account number: 611140175, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](number_digits_to_list(611140175, 9)))

        # Account number: 611140176, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](number_digits_to_list(611140176, 9)))

        # Account number: 11140175, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](number_digits_to_list(11140175, 8)))

        # Account number: 11140154 (branch number 154, remainder of 2 is valid)
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](number_digits_to_list(11140154, 8)))

        # Account number: 11140200 (branch number not listed, remainder of 2 is invalid)
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](number_digits_to_list(11140200, 8)))

    def test_jerusalem_validator(self):
        # For Bank Jerusalem, there is no validation for the account numbers. So, all numbers should be valid

        # Account number: 123456789, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](number_digits_to_list(123456789, 9)))

        # Account number: 987654321, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](number_digits_to_list(987654321, 9)))

        # Account number: 111111111, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](number_digits_to_list(111111111, 9)))

        # Account number: 222222222, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](number_digits_to_list(222222222, 9)))

        # Account number: 333333333, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](number_digits_to_list(333333333, 9)))



if __name__ == "__main__":
    unittest.main()
