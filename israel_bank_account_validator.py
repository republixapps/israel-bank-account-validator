import logging
from typing import Union

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_BANKS = {
    'YAHAV': 4,
    'ISRAEL_POST': 9,
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
MIZRAHI_TEFAHOT_BRANCH_THRESHOLD = 400
MIZRAHI_TEFAHOT_BRANCH_THRESHOLD_MIN = 401
MIZRAHI_TEFAHOT_BRANCH_THRESHOLD_MAX = 799

LEUUMI_BRANCH_THRESHOLD_LIST = [800, 864]


def convert_to_int(input_value):
    try:
        if isinstance(input_value, str):
            return int(input_value)
        return input_value
    except Exception as e:
        logger.error(e)
        raise ValueError('Could not convert to int')


def scalar_product(arr1, arr2):
    return sum(a * b for a, b in zip(arr1, arr2))


def number_digits_to_list(num, length):
    return [int(x) for x in str(num).zfill(length)]


def is_positive_integer(num):
    return isinstance(num, int) and num >= 0


class BankNumberValueError(Exception):
    pass


class BankBranchNumberValueError(Exception):
    pass


class BankAccountNumberValueError(Exception):
    pass


class UnsupportedBankError(Exception):
    pass


def validate_bank_account(bank_number: Union[int, str], branch_number: Union[int, str],
                          account_number: Union[int, str]) -> bool:
    try:
        # Convert to integers if necessary
        bank_number = convert_to_int(bank_number)
    except ValueError:
        raise BankNumberValueError('Bank number could not be converted to an integer')
    try:
        branch_number = convert_to_int(branch_number)
    except ValueError:
        raise BankBranchNumberValueError('Branch number could not be converted to an integer')
    try:
        account_number = convert_to_int(account_number)
    except ValueError:
        raise BankAccountNumberValueError('Account number could not be converted to an integer')

    if not is_positive_integer(bank_number):
        raise BankNumberValueError('Bank number is not valid, negative integer')

    # Check if bank is supported
    if bank_number not in SUPPORTED_BANKS.values():
        logger.error('Unsupported bank number')
        raise UnsupportedBankError('Unsupported bank number')

    if not is_positive_integer(branch_number):
        raise BankBranchNumberValueError('Branch number is not valid, negative integer')
    if not is_positive_integer(account_number):
        raise BankAccountNumberValueError('Account number is not valid, negative integer')

    # Get the appropriate validator for the given bank
    validator = BANK_VALIDATORS.get(bank_number)
    if validator is None:
        raise UnsupportedBankError('Unsupported bank number')

    account_number_digits = number_digits_to_list(account_number, 9)
    branch_number_digits = number_digits_to_list(branch_number, 3)

    # Apply the bank-specific validation rule
    return validator(branch_number, account_number_digits, branch_number_digits)


# Define the validator functions depending on the specific rules for each bank.
def yahav_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[3:9], [6, 5, 4, 3, 2, 1])
    sum_val += scalar_product(branch_number_digits[:4], [9, 8, 7])
    remainder = sum_val % 11
    return remainder in [0, 2]


def israel_post_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:9], [9, 8, 7, 6, 5, 4, 3, 2, 1])
    remainder = sum_val % 10
    return remainder == 0


def discount_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:9], [9, 8, 7, 6, 5, 4, 3, 2, 1])
    remainder = sum_val % 11
    return remainder in [0, 2, 4]


def hapoalim_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[3:9], [6, 5, 4, 3, 2, 1])
    sum_val += scalar_product(branch_number_digits[:4], [9, 8, 7])
    remainder = sum_val % 11
    return remainder in [0, 2, 4, 6]


def igud_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[1:9], [7, 6, 5, 4, 3, 2])
    sum_val += scalar_product(branch_number_digits[:4], [10, 9, 8])
    sum_val += account_number_digits[7] * 10 + account_number_digits[8]  # add to sum control digits
    remainder = sum_val % 100
    return remainder in [90, 72, 70, 60, 20]


def otsar_hahayal_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[3:], [6, 5, 4, 3, 2, 1])
    sum_val += scalar_product(branch_number_digits[:4], [9, 8, 7])
    remainder = sum_val % 11

    if remainder == 0:
        return True
    if remainder in [0, 2] and branch_number in [385, 384, 365, 347, 363, 362, 361]:
        return True
    elif remainder == 4 and branch_number in [363, 362, 361]:
        return True

    return False


def one_zero_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    if branch_number == 0:
        branch_number = 1
    if branch_number_digits[-1] == 0:
        branch_number_digits[-1] = 1

    # Combine the digits into a single number
    check_number = int(''.join(map(str, branch_number_digits + account_number_digits[:-2])))

    remainder = check_number % 97
    calculated_control_digits = 98 - remainder

    original_control_digits = account_number_digits[7] * 10 + account_number_digits[8]
    return calculated_control_digits == original_control_digits


def leumi_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    # Account types
    account_types = [110, 128, 180, 330, 340]

    # Multipliers for branch and account number digits
    account_multipliers = [7, 6, 5, 4, 3, 2]
    branch_multipliers = [10, 9, 8]

    # Step 1: Multiply digits by their respective multipliers and add the products together
    total = scalar_product(account_number_digits[1:7], account_multipliers)
    total += scalar_product(branch_number_digits[:4], branch_multipliers)

    is_skip_110_account_type = False
    account_number_digits_threshold = account_number_digits[7] + account_number_digits[6] * 10
    if branch_number in LEUUMI_BRANCH_THRESHOLD_LIST and account_number_digits_threshold not in [20, 23, 0] or \
            branch_number not in LEUUMI_BRANCH_THRESHOLD_LIST and account_number_digits_threshold != 0:
        is_skip_110_account_type = True

    # Step 2: Add each account type to the total and check against the control digits
    control_digits = account_number_digits[7:9]
    for account_type in account_types:
        # Skip account type 110 if the 5th and 6th digits do not match certain criteria
        if account_type == 110 and is_skip_110_account_type:
            continue
        check_total = total + account_type
        # Step 3: Calculate the difference between 100 and the last two digits of check_total
        last_two_digits = check_total % 100
        check_digits_value = 100 - last_two_digits if last_two_digits != 0 else last_two_digits
        check_digits = [check_digits_value // 10, check_digits_value % 10]
        # If the check digits match the control digits, the account number is valid
        if check_digits == control_digits:
            return True

    # If none of the account types produce a match, the account number is not valid
    return False


def mizrahi_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    if MIZRAHI_TEFAHOT_BRANCH_THRESHOLD_MIN <= branch_number <= MIZRAHI_TEFAHOT_BRANCH_THRESHOLD_MAX:
        branch_number -= MIZRAHI_TEFAHOT_BRANCH_THRESHOLD
        branch_number_digits = number_digits_to_list(branch_number, 3)

    sum_val = scalar_product(account_number_digits[3:9], [6, 5, 4, 3, 2, 1])
    sum_val += scalar_product(branch_number_digits[:4], [9, 8, 7])
    remainder = sum_val % 11
    return remainder in [0, 2, 4]


def citybank_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    # Multiply each digit by its factor and sum the results
    sum_val = scalar_product(account_number_digits[:8], [3, 2, 7, 6, 5, 4, 3, 2])
    remainder = sum_val % 11
    calculated_control_digit = (11 - remainder) % 10  # the %10 operation ensures the result is a single digit

    original_control_digit = account_number_digits[8]

    # Return True if the calculated check digit matches the original check digit, otherwise return False
    return calculated_control_digit == original_control_digit


def hsbc_validator(branch_number, account_number_digit, branch_number_digits) -> bool:
    return (branch_number == 101 and account_number_digit[6] == 4 or branch_number == 102
            and account_number_digit[-3:] == [0, 0, 1])


def beinleumi_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    sum_val = scalar_product(account_number_digits[:9], [9, 8, 7, 6, 5, 4, 3, 2, 1])
    remainder = sum_val % 11
    if remainder in [0, 6]:
        return True
    else:
        sum_val = scalar_product(account_number_digits[3:], [6, 5, 4, 3, 2, 1])
        remainder = sum_val % 11
        return remainder in [0, 6]


def masad_validator(branch_number, account_number_digits, branch_number_digits) -> bool:
    # Branches with 0 or 2 remainder are considered valid
    special_branches = [154, 166, 178, 181, 183, 191, 192, 503, 505, 507, 515, 516, 527, 539]

    # Multipliers for account and branch number digits
    account_multipliers = [6, 5, 4, 3, 2, 1]
    branch_multipliers = [9, 8, 7]

    # Calculate the total of multiplied digits
    sum_val = scalar_product(account_number_digits[3:9], account_multipliers)
    sum_val += scalar_product(branch_number_digits[:3], branch_multipliers)

    remainder = sum_val % 11

    # The total should be divisible by 11, unless the branch number is in the special list
    if remainder == 0 or (branch_number in special_branches and remainder == 2):
        return True

    return False


def jerusalem_validator(account_number, branch_number, branch_number_digits) -> bool:
    return True


BANK_VALIDATORS = {
    SUPPORTED_BANKS['YAHAV']: yahav_validator,
    SUPPORTED_BANKS['ISRAEL_POST']: israel_post_validator,
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
