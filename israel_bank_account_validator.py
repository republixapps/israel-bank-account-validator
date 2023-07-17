import logging
from typing import Union

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_BANKS = {
    'YAHAV': 4,
    'POST': 9,
    'LEUMI': 10,
    'DISCOUNT': 11,
    'HAPOALIM': 12,
    'IGUD': 13,
    'OTSAR_HAHAYAL': 14,
    'MERCANTILE': 17,
    'ONE_ZERO': 18,
    'MIZRAHI_TEFAHOT': 20,
    'CITYBANK': 22,
    'HSBC': 23,
    'BEINLEUMI': 31,
    'ARAVEI_ISRAELI': 34,
    'MASAD': 46,
    'POALEI_AGUDAT_ISRAEL': 52,
    'JERUSALEM': 54
}

# Constants
MIZRAHI_TEFAHOT_THRESHOLD = 400
MIZRAHI_BANK_NUMBER_THRESHOLD_MIN = 401
MIZRAHI_BANK_NUMBER_THRESHOLD_MAX = 799


def validate_bank_account(bank_number: Union[int, str], branch_number: Union[int, str],
                          account_number: Union[int, str]) -> bool:
    try:
        # Convert to integers if necessary
        bank_number = convert_to_int(bank_number)
        branch_number = convert_to_int(branch_number)
        account_number = convert_to_int(account_number)
    except ValueError:
        logger.error("One or more inputs could not be converted to an integer")
        return False

    # Check if bank is supported
    if bank_number not in SUPPORTED_BANKS.values():
        logger.error("Unsupported bank number")
        return False

    if not is_non_negative_integer(bank_number) or not is_non_negative_integer(
            branch_number) or not is_non_negative_integer(account_number):
        logger.error("One or more inputs are not non-negative integers")
        return False

    # Get the appropriate validator for the given bank
    validator = BANK_VALIDATORS.get(bank_number)
    if validator is None:
        logger.error("No validator found for the given bank")
        return False

    account_number_digits = number_digits_to_list(account_number, 9)
    branch_number_digits = number_digits_to_list(branch_number, 3)

    # Apply the bank-specific validation rule
    return validator(branch_number, account_number_digits, branch_number_digits)


# Define the validator functions for each bank
# NOTE: The implementation of these functions depends on the specific rules for each bank.
# I've left the bodies of these functions empty because I don't have the exact rules.
def yahav_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
    sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
    remainder = sum_val % 11
    return remainder in [0, 2]


def post_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    remainder = sum_val % 10
    return remainder == 0


def discount_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    remainder = sum_val % 11
    return remainder in [0, 2, 4]


def hapoalim_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
    sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
    remainder = sum_val % 11
    return remainder in [0, 2, 4, 6]


def igud_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:8], [1, 10, 2, 3, 4, 5, 6, 7])
    sum_val += scalar_product(branch_number_digits[:4], [8, 9, 10])
    remainder = sum_val % 100
    return remainder in [90, 72, 70, 60, 20]


def otsar_hahayal_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
    sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
    remainder = sum_val % 11

    if remainder == 0:
        return True
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


def one_zero_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    # Combine the digits into a single number
    check_number = int(''.join(map(str, branch_number_digits + account_number_digits[:-2])))

    # Calculate the check digits
    remainder = check_number % 97
    check_digits_calculated = 98 - remainder

    # Extract the original check digits
    check_digits_original = account_number_digits[-2:]

    # Return True if the calculated check digits match the original check digits, otherwise return False
    return check_digits_calculated == check_digits_original


def leumi_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    # Account types
    account_types = [110, 128, 180, 330, 340]

    # Multipliers for branch and account number digits
    account_multipliers = [2, 3, 4, 5, 6, 7]
    branch_multipliers = [8, 9, 10]

    # Step 1: Multiply digits by their respective multipliers and add the products together
    total = scalar_product(account_number_digits[:8], account_multipliers)
    total += scalar_product(branch_number_digits[:4], branch_multipliers)

    # Step 2: Add each account type to the total and check against the control digits
    control_digits = branch_number_digits[-2:]
    for account_type in account_types:
        # Skip account type 110 if the 5th and 6th digits do not match certain criteria
        if account_type == 110 and (account_number_digits[4:6] not in [[2, 0], [2, 3], [0, 0], [8, 0]]):
            continue
        check_total = total + account_type
        # Step 3: Calculate the difference between 100 and the last two digits of check_total
        check_digits = [(check_total // 10 ** i) % 10 for i in reversed(range(2))]
        # If the check digits match the control digits, the account number is valid
        if check_digits == control_digits:
            return True

    # If none of the account types produce a match, the account number is not valid
    return False


def mizrahi_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    if MIZRAHI_BANK_NUMBER_THRESHOLD_MIN <= branch_number <= MIZRAHI_BANK_NUMBER_THRESHOLD_MAX:
        branch_number -= MIZRAHI_TEFAHOT_THRESHOLD
    sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
    sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
    remainder = sum_val % 11
    return remainder in [0, 2, 4]


def citybank_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    # Multiply each digit by its factor and sum the results
    sum_val = scalar_product(account_number_digits[:-1], [2, 3, 4, 5, 6, 7, 2, 3])

    # Calculate the remainder when divided by 11
    remainder = sum_val % 11

    # Calculate the check digit
    check_digit_calculated = (11 - remainder) % 10  # the %10 operation ensures the result is a single digit

    # Extract the original check digit
    check_digit_original = account_number_digits[-1]

    # Return True if the calculated check digit matches the original check digit, otherwise return False
    return check_digit_calculated == check_digit_original


def hsbc_validator(branch_number, account_number_digit, branch_number_digits) -> bool:
    if branch_number == 101:
        # The seventh digit from the left should be 4
        if account_number_digit[2] != 4:
            return False

    elif branch_number == 102:
        # There is only one valid account number: 001
        if account_number_digit[-3:] != [0, 0, 1]:
            return False

    # If no rules were broken, the account number is valid
    return True


def beinleumi_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    remainder = sum_val % 11
    if remainder in [0, 6]:
        return True
    else:
        sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
        remainder = sum_val % 11
        return remainder in [0, 6]


def masad_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:6], [1, 2, 3, 4, 5, 6])
    sum_val += scalar_product(branch_number_digits[:4], [7, 8, 9])
    remainder = sum_val % 11

    if remainder == 0:
        return True

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


def jerusalem_validator(account_number, branch_number, branch_number_digits) -> bool:
    return True


# A dictionary mapping bank numbers to their specific validation functions
BANK_VALIDATORS = {
    SUPPORTED_BANKS['YAHAV']: yahav_validator,
    SUPPORTED_BANKS['POST']: post_validator,
    SUPPORTED_BANKS['LEUMI']: leumi_validator,
    SUPPORTED_BANKS['DISCOUNT']: discount_validator,
    SUPPORTED_BANKS['HAPOALIM']: hapoalim_validator,
    SUPPORTED_BANKS['IGUD']: igud_validator,
    SUPPORTED_BANKS['OTSAR_HAHAYAL']: otsar_hahayal_validator,
    SUPPORTED_BANKS['MERCANTILE']: discount_validator,
    SUPPORTED_BANKS['ONE_ZERO']: one_zero_validator,
    SUPPORTED_BANKS['MIZRAHI_TEFAHOT']: mizrahi_validator,
    SUPPORTED_BANKS['CITYBANK']: citybank_validator,
    SUPPORTED_BANKS['HSBC']: hsbc_validator,
    SUPPORTED_BANKS['BEINLEUMI']: beinleumi_validator,
    SUPPORTED_BANKS['ARAVEI_ISRAELI']: leumi_validator,
    SUPPORTED_BANKS['MASAD']: masad_validator,
    SUPPORTED_BANKS['POALEI_AGUDAT_ISRAEL']: beinleumi_validator,
    SUPPORTED_BANKS['JERUSALEM']: jerusalem_validator,
}

def convert_to_int(input_value):
    if isinstance(input_value, str):
        return int(input_value)
    return input_value


def scalar_product(arr1, arr2):
    return sum(a * b for a, b in zip(arr1, arr2))


def number_digits_to_list(num, length):
    return [int(x) for x in str(num).zfill(length)]

def is_non_negative_integer(num):
    return isinstance(num, int) and num >= 0


print(validate_bank_account(12, 345, 67890))
print(validate_bank_account(11, 345, 67890))
print(validate_bank_account(20, 345, 67890))
print(validate_bank_account(10, 345, 67890))
print(validate_bank_account(9, 345, 67890))
print(validate_bank_account(13, 345, 67890))
