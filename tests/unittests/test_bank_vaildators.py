import unittest

from israel_bank_account_validator import BANK_VALIDATORS, SUPPORTED_BANKS, number_digits_to_list


class TestBankValidators(unittest.TestCase):
    def test_yahav_validator(self):
        # Example from MASAV doc, Account number: 050067, Branch number: 284, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](482, number_digits_to_list(50067, 9),
                                                                  number_digits_to_list(284, 3)))

        # Account number: 760051, Branch number: 482, should be invalid as we changed a digit
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](482, number_digits_to_list(760051, 9),
                                                                   number_digits_to_list(482, 3)))

        # Account number: 000000, Branch number: 9, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](9, number_digits_to_list(000000, 9),
                                                                   number_digits_to_list(9, 3)))

        # Account number: 050067, Branch number: 000, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['YAHAV']](0, number_digits_to_list(50067, 9),
                                                                  number_digits_to_list(0, 3)))

    def test_israel_post_validator(self):
        # Example from MASAV doc, Account number: 059121900, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['ISRAEL_POST']](None, number_digits_to_list(59121900, 9), None))

        # Account number: 9121951, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['ISRAEL_POST']](None, number_digits_to_list(9121951, 9), None))

        # Account number: 000000000, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['ISRAEL_POST']](None, number_digits_to_list(0, 9), None))

    def test_leumi_validator(self):
        # Example from MASAV doc, Account number: 07869660, Branch number: 936, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](936, number_digits_to_list(7869660, 9),
                                                                  number_digits_to_list(936, 3)))

        # Account number: 06696871, Branch number: 936, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](639, number_digits_to_list(6696871, 9),
                                                                   number_digits_to_list(639, 3)))

        # Account number: 99696203, Branch number: 800, prevent skipping account_type 110, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](800, number_digits_to_list(99696203, 9),
                                                                  number_digits_to_list(8, 3)))

        # Account number: 99696230, Branch number: 801, skipping account_type 110, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](801, number_digits_to_list(2696230, 9),
                                                                   number_digits_to_list(8, 3)))

        # Account number: 90054318, Branch number: 912, prevent skipping account_type 110, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](912, number_digits_to_list(81345047, 9),
                                                                  number_digits_to_list(912, 3)))

        # Account number: 00000000, Branch number: 800, prevent skipping account_type 110, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['LEUMI']](800, number_digits_to_list(0, 9),
                                                                   number_digits_to_list(800, 3)))

    def test_discount_validator(self):
        # Example from MASAV doc, Account number: 000032018, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['DISCOUNT']](None, number_digits_to_list(32018, 9), None))

        # Account number: 100032018, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['DISCOUNT']](None, number_digits_to_list(132018, 9), None))

    def test_hapoalim_validator(self):
        # Example from MASAV doc - Test reminder 0, Account number: 041116, Branch number: 571, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](571, number_digits_to_list(41116, 9),
                                                                     number_digits_to_list(571, 3)))

        # Test reminder 2, Account number: 011143, Branch number: 175, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](175, number_digits_to_list(11143, 9),
                                                                      number_digits_to_list(175, 3)))

        # Test reminder 4, Account number: 011145, Branch number: 678, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](678, number_digits_to_list(11145, 9),
                                                                     number_digits_to_list(678, 3)))

        # Test reminder 6, Account number: 011147, Branch number: 678, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](678, number_digits_to_list(11147, 9),
                                                                     number_digits_to_list(678, 3)))

        # Test invalid - reminder 7, Account number: 542117, Branch number: 678, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HAPOALIM']](14, number_digits_to_list(542117, 9),
                                                                      number_digits_to_list(14, 3)))

    def test_igud_validator(self):
        # Example from MASAV doc - Test reminder 90, Account number: 11710022, branch number: 607, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](607, number_digits_to_list(11710022, 9),
                                                                 number_digits_to_list(607, 3)))

        # Test reminder 72, Account number: 22001711, branch number: 706, should be invalid as we changed a digit
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](706, number_digits_to_list(22001711, 9),
                                                                 number_digits_to_list(706, 3)))

        # Test reminder 70, Account number: 22001710, branch number: 706, should be invalid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](706, number_digits_to_list(22001709, 9),
                                                                 number_digits_to_list(706, 3)))

        # Test reminder 60, Account number: 22000702, branch number: 706, should be invalid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](706, number_digits_to_list(22000702, 9),
                                                                 number_digits_to_list(706, 3)))

        # Test reminder 20, Account number: 22001759, branch number: 706, should be invalid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](706, number_digits_to_list(22001759, 9),
                                                                 number_digits_to_list(706, 3)))

        # Test invalid reminder 74, Account number: 11710022, branch number: 000, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['IGUD']](0, number_digits_to_list(11710022, 9),
                                                                  number_digits_to_list(0, 3)))

    def test_otsar_ahayal_validator(self):
        # Example from MASAV doc, Account number: 041116, branch number: 571, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](571, number_digits_to_list(41116, 6),
                                                                          number_digits_to_list(571, 3)))

        # Account number: 141116, branch number: 571, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](571, number_digits_to_list(141116, 6),
                                                                           number_digits_to_list(571, 3)))

        # Test one of 385/384/365/374 branches, Account number: 041118, branch number: 384, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](384, number_digits_to_list(41118, 6),
                                                                          number_digits_to_list(384, 3)))

        # Test one of 385, 384, 365, 374 branches, Account number: 041114, branch number: 384, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](384, number_digits_to_list(41114, 6),
                                                                           number_digits_to_list(384, 3)))

        # Test one of 363, 362, 361 branches, Account number: 041110, branch number: 384, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](363, number_digits_to_list(41110, 6),
                                                                          number_digits_to_list(363, 3)))

        # Test one of 363, 362, 361 branches, Account number: 041116, branch number: 384, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['OTSAR_HAHAYAL']](363, number_digits_to_list(41116, 6),
                                                                           number_digits_to_list(363, 3)))

    def test_one_zero_validator(self):
        # Example from MASAV doc, Account number: 123456771, branch number: 001, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](None, number_digits_to_list(123456771, 9),
                                                                     number_digits_to_list(1, 3)))

        # Account number: 123456772, branch number: 001, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](None, number_digits_to_list(123456772, 9),
                                                                      number_digits_to_list(1, 3)))

        # Account number: 000000000, branch number: 001, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](None, number_digits_to_list(0, 9),
                                                                      number_digits_to_list(1, 3)))

        # Account number: 000000000, branch number: 000, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['ONE_ZERO']](None, number_digits_to_list(0, 9),
                                                                      number_digits_to_list(0, 3)))

    def test_mizrahi_validator(self):
        # Example from MASAV doc - Test reminder of 0, Account number: 160778, Branch number: 006, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](6, number_digits_to_list(160778, 9),
                                                                            number_digits_to_list(6, 3)))

        # Test reminder of 2, Account number: 160776, Branch number: 106, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](106, number_digits_to_list(160771, 9),
                                                                            number_digits_to_list(106, 3)))

        # Test reminder of 4, Account number: 160779, Branch number: 126, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](126, number_digits_to_list(160779, 9),
                                                                            number_digits_to_list(126, 3)))

        # Test invalid reminder 1, Account number: 160779, Branch number: 006, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['MIZRAHI_TEFAHOT']](6, number_digits_to_list(160779, 9),
                                                                             number_digits_to_list(6, 3)))

    def test_citybank_validator(self):
        # Example from MASAV doc, Account number: 700241017, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['CITYBANK']](None, number_digits_to_list(700241017, 9), None))

        # Account number: 700241317, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['CITYBANK']](None, number_digits_to_list(700241317, 9), None))

    def test_hsbc_validator(self):
        # For branch 101, account number should have 7th digit from the left as 4
        # Account number: 123456489,  branch: 101, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](101, number_digits_to_list(123456489, 9), None))

        # Account number: 123356789, branch: 101, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](101, number_digits_to_list(123356789, 9), None))

        # For branch 102, account number should end with 001 control digits
        # Account number: 123456001, branch: 102, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](102, number_digits_to_list(123456001, 9), None))

        # Account number: 123456010, branch: 102, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](102, number_digits_to_list(123456010, 9), None))

        # No special rules for other branches, Account number: 123356789, branch: 121, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](121, number_digits_to_list(123356789, 9), None))

        # No special rules for other branches, Account number: 123456010, branch: 121, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['HSBC']](121, number_digits_to_list(123456010, 9), None))

    def test_beinleumi_validator(self):
        # Example from MASAV doc - Test reminder = 0 on first rule, Account number: 000032018, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](None, number_digits_to_list(32018, 9), None))

        # Test reminder = 6 on first rule, Account number: 000132018, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](None, number_digits_to_list(132018, 9), None))

        # Test reminder = 0 on second rule, Account number: 007232017, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](None, number_digits_to_list(7232017, 9), None))

        # Test reminder = 6 on second rule, Account number: 006132018, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](None, number_digits_to_list(6132018, 9), None))

        # Test invalid, reminder = 7 on first and second rules, Account number: 000132019, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](None, number_digits_to_list(132019, 9), None))

        # Test invalid, reminder = 7 on first rule, Account number: 007132019, should be valid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['BEINLEUMI']](None, number_digits_to_list(7132019, 9), None))

    def test_masad_validator(self):
        # For Masad, the sum of each digit multiplied by its position (starting from 1)
        # should be divisible by 11 with no remainder except for specific branch numbers,
        # where remainders of 0 and 2 are also valid.

        # Example from MASAV doc - Test reminder 0, Account number: 041116, branch number: 571, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](571, number_digits_to_list(41116, 9),
                                                                  number_digits_to_list(571, 3)))

        # Test reminder 0 on special branch 505, Account number: 241110, branch number: 505, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](505, number_digits_to_list(241110, 9),
                                                                  number_digits_to_list(505, 3)))

        # Test reminder 2 on special branch 505, Account number: 241112, branch number: 505, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](505, number_digits_to_list(241112, 9),
                                                                  number_digits_to_list(505, 3)))

        # Test invalid reminder 5 on special branch 505, Account number: 041116, branch number: 505, should be invalid
        self.assertFalse(BANK_VALIDATORS[SUPPORTED_BANKS['MASAD']](505, number_digits_to_list(41116, 9),
                                                                   number_digits_to_list(505, 3)))

    def test_jerusalem_validator(self):
        # For Bank Jerusalem, there is no validation for the account numbers. So, all numbers should be valid

        # Account number: 123456789, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](None, number_digits_to_list(123456789, 9), None))

        # Account number: 987654321, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](None, number_digits_to_list(987654321, 9), None))

        # Account number: 111111111, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](None, number_digits_to_list(111111111, 9), None))

        # Account number: 22, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](None, number_digits_to_list(22, 9), None))

        # Account number: 3, should be valid
        self.assertTrue(BANK_VALIDATORS[SUPPORTED_BANKS['JERUSALEM']](None, number_digits_to_list(3, 9), None))


if __name__ == "__main__":
    unittest.main()
