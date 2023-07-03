import logging
from typing import Union

logger = logging.getLogger(__name__)


SUPPORTED_BANKS = {
    'YAHAV': 4,
    'POST': 9,
    'LEUMI': 10,
    'DISCOUNT': 11,
    'HAPOALIM': 12,
    'IGUD': 13,
    'OTSAR_AHAYAL': 14,
    'MERCANTILE': 17,
    'MIZRAHI_TEFAHOT': 20,
    'CITIBANK': 22,
    'BEINLEUMI': 31,
    'ARAVEI_ISRAELI': 34,
    'MASAD': 46,
    'POALEI_AGUDAT_ISRAEL': 52
}


def validate_bank_account(
        bank_number: Union[int, str],
        branch_number: Union[int, str],
        account_number: Union[int, str]) -> bool:

    if isinstance(bank_number, str):
        bank_number = int(bank_number)
    if isinstance(branch_number, str):
        branch_number = int(branch_number)
    if isinstance(account_number, str):
        account_number = int(account_number)

    if not is_non_negative_integer(bank_number):
        return False
    if not is_non_negative_integer(branch_number):
        return False
    if not is_non_negative_integer(account_number):
        return False

    if bank_number == SUPPORTED_BANKS['MIZRAHI_TEFAHOT']:
        if branch_number > 400:
            branch_number -= 400

    account_number_digits = number_digits_to_list(account_number, 9)
    branch_number_digits = number_digits_to_list(branch_number, 3)

    # Account number validation
    sum_val = 0
    remainder = 0
    if bank_number in {SUPPORTED_BANKS['LEUMI'], SUPPORTED_BANKS['IGUD'], SUPPORTED_BANKS['ARAVEI_ISRAELI']}:
        sum_val = scalar_product(account_number_digits[:8], [1, 10, 2, 3, 4, 5, 6, 7])
        sum_val += scalar_product(branch_number_digits[:4], [8, 9, 10])
        remainder = sum_val % 100
        return remainder in [90, 72, 70, 60, 20]

    elif bank_number in {SUPPORTED_BANKS['YAHAV'], SUPPORTED_BANKS['MIZRAHI_TEFAHOT'], SUPPORTED_BANKS['HAPOALIM']}:
        sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
        sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
        remainder = sum_val % 11

        if bank_number == SUPPORTED_BANKS['YAHAV']:
            return remainder in [0, 2]
        elif bank_number == SUPPORTED_BANKS['MIZRAHI_TEFAHOT']:
            return remainder in [0, 2, 4]
        elif bank_number == SUPPORTED_BANKS['HAPOALIM']:
            return remainder in [0, 2, 4, 6]

    elif bank_number in {
            SUPPORTED_BANKS['DISCOUNT'],
            SUPPORTED_BANKS['MERCANTILE'],
            SUPPORTED_BANKS['BEINLEUMI'],
            SUPPORTED_BANKS['POALEI_AGUDAT_ISRAEL']}:

        sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        remainder = sum_val % 11

        if bank_number in [SUPPORTED_BANKS['DISCOUNT'], SUPPORTED_BANKS['MERCANTILE']]:
            return remainder in [0, 2, 4]
        elif bank_number in [SUPPORTED_BANKS['BEINLEUMI'], SUPPORTED_BANKS['POALEI_AGUDAT_ISRAEL']]:
            if remainder in [0, 6]:
                return True
            else:
                sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
                remainder = sum_val % 11
                return remainder in [0, 6]

    elif bank_number == SUPPORTED_BANKS['POST']:
        sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        remainder = sum_val % 10
        return remainder == 0

    elif bank_number == 54:
        return True

    elif bank_number == SUPPORTED_BANKS['CITIBANK']:
        sum_val = scalar_product(account_number_digits[1:9], [2, 3, 4, 5, 6, 7, 2, 3])
        return (11 - sum_val % 11) == account_number_digits[0]

    elif bank_number in [SUPPORTED_BANKS['OTSAR_AHAYAL'], SUPPORTED_BANKS['MASAD']]:
        sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
        sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
        remainder = sum_val % 11

        if remainder == 0:
            return True

        if bank_number == SUPPORTED_BANKS['MASAD']:
            if remainder == 2 and branch_number in [
                    154, 166, 178, 181, 183, 191, 192, 503, 505, 507, 515, 516, 527, 539]:
                return True

            sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            remainder = sum_val % 11

            if remainder == 0:
                return True
            else:
                sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
                remainder = sum_val % 11
                return remainder == 0

        if bank_number == SUPPORTED_BANKS['OTSAR_AHAYAL']:
            if remainder in [0, 2] and branch_number in [385, 384, 365, 347, 363, 362, 361]:
                return True
            elif remainder == 4 and branch_number in [363, 362, 361]:
                return True
            else:
                sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
                remainder = sum_val % 11
                if remainder == 0:
                    return True
                else:
                    sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
                    remainder = sum_val % 11
                    return remainder == 0

    return False


def scalar_product(arr1, arr2):
    product = 0
    for i in range(min(len(arr1), len(arr2))):
        product += arr1[i] * arr2[i]
    return product


def number_digits_to_list(num, length):
    digits_array = []
    for _ in range(length):
        digits_array.append(num % 10)
        num = num // 10
    return digits_array


def is_non_negative_integer(num):
    return isinstance(num, int) and num >= 0


print(validate_bank_account(12, 345, 67890))
print(validate_bank_account(11, 345, 67890))
print(validate_bank_account(20, 345, 67890))
print(validate_bank_account(10, 345, 67890))
print(validate_bank_account(9, 345, 67890))
print(validate_bank_account(13, 345, 67890))
