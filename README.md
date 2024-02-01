# Israel Bank Account Validator
Based on the MASAV bank account validation documentation (available [here](https://www.masav.co.il/media/2473/bdikat_hukiot_heshbon.pdf)), this package provides functions and classes to validate Israeli bank account numbers for supported banks.

## Features
Validates bank account numbers for various supported Israeli banks.
Provides detailed logging for easy debugging.
Supports multiple data types (integers or strings) for input.
Offers specific exceptions for different error scenarios.
Supported Banks
Currently, the supported banks are:

+ YAHAV
+ ISRAEL_POST
+ LEUMI
+ DISCOUNT
+ HAPOALIM
+ IGUD
+ OTSAR_HAHAYAL
+ MERCANTILE
+ ONE_ZERO
+ MIZRAHI_TEFAHOT
+ CITYBANK
+ HSBC
+ BEINLEUMI
+ ARAVEI_ISRAELI
+ MASAD
+ POALEI_AGUDAT_ISRAEL
+ JERUSALEM

## Installation
You can install this package using pip:

```bash
pip install git+https://github.com/republixapps/israel-bank-account-validator.git@rc#egg=israel_bank_account_validator
```

# Usage
Import the required functions and classes and use the validate_bank_account function:

```python
from bank_validations import validate_bank_account
from bank_validations import InvalidBankAccount, ValidBankAccount

try:
    bank_code = "012"
    branch_code = "345"
    account_number = "67890"
    validate_bank_account(bank_code, branch_code, account_number)

except KeyError:
    print("Bank code or branch code not found in database.")
except InvalidBankAccount:
    print("Bank account is invalid.")
except ValidBankAccount:
    print("Bank account is valid.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

You can also call individual bank validators:
```python
from israel_bank_account_validator import leumi_validator, number_digits_to_list
account_to_digits = number_digits_to_list(account_number, 9)  # 07869660
branch_to_digits = number_digits_to_list(branch_number, 3)
isValid = leumi_validator(branch_number, account_to_digits, branch_to_digits)
print(isValid) # prints either True or False
```

# Running Tests
This package comes with two test suites:

+ test_bank_validators.py - Tests the validation logic for each individual bank.
+ test_bank_account_validation.py - Tests the overall account validation function.
To run the tests, ensure you have pytest installed:

To run the tests, ensure you have pytest installed:
```bash
pip install pytest
```

Then run the tests using the following:

```bash
pytest test_bank_validators.py
pytest test_bank_account_validation.py
````
Test cases are sourced from JSON files, ensuring easy maintenance and expansion.
+ test_bank_account_data.json - Contains test cases for the overall account validation function.
+ test_bank_validators_data.json - Contains test cases for each individual bank validation function.

## Error Handling
The package provides specific exceptions for various error scenarios:

+ BankNumberValueError: Raised when the bank number is invalid.
+ BankBranchNumberValueError: Raised when the branch number is invalid.
+ BankAccountNumberValueError: Raised when the account number is invalid.
+ UnsupportedBankError: Raised when the provided bank is not supported.

# License
This library is licensed under the MIT License.