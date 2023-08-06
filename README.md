# Israel Bank Account Validator

This Python library is a copy of the original JavaScript library found at [il-bank-account-validator](https://github.com/soryy708/il-bank-account-validator). The initial conversion was performed by an AI model (chatGPT), with subsequent refactoring and reorganization carried out to enhance the functionality and usability of the library.

This library is designed in accordance with the MASAV Bank account validation rules, which can be found in the [following documentation](https://masav.co.il/media/2473/bdikat_hukiot_heshbon.pdf) (last updated on 04/04/2022). It supports all the banks in Israel that comply with the MASAV guidelines.

## Features

- A comprehensive `validate_bank_account()` function
- Individual validators for each bank
- Utility functions to assist in bank account validation

## Installation

To install this library, you can use pip:

```bash
pip install israel-bank-account-validator
```

# Usage
To use this library, you can import it and call the validate_bank_account() function:
```python
from israel_bank_account_validator import validate_bank_account

isValid = validate_bank_account(bank_number, bank_branch_number, account_number)
print(isValid) # prints either True or False
```

You can also call individual bank validators:
```python
from israel_bank_account_validator import leumi_validator, number_digits_to_list
account_to_digits = number_digits_to_list(account_number, 9)  # 07869660
branch_to_digits = number_digits_to_list(branch_number, 3)
isValid = leumi_validator(branch_number, account_to_digits, branch_to_digits)
print(isValid) # prints either True or False
```

# Key Functions
validate_bank_account(bank_number, bank_branch_number, account_number)
This is the main function, which you can use to validate any Israeli bank account number.

# Example:
```python
from israel_bank_account_validator import validate_bank_account

if validate_bank_account('11', '111', '1111111'):
    print("The bank account number is valid.")
else:
    print("The bank account number is invalid.")
```

You can also call individual bank validators:
```python
from israel_bank_account_validator import leumi_validator, number_digits_to_list
branch_number = 936
account_number = 7869660
account_to_digits = number_digits_to_list(7869660, 9)  # 07869660
branch_to_digits = number_digits_to_list(936, 3)

if leumi_validator(branch_number, account_to_digits, branch_to_digits):
    print("The bank account number is valid.")
else:
    print("The bank account number is invalid.")
```

# Other Validator Functions
The library also includes individual validator functions for each bank. These functions follow the naming convention validate_bank_number_X where X is the bank code.

# Testing
To run the tests, you can use Python's built-in unittest module or pytest.

# Using Unittest
Navigate to the directory containing the tests and run the unittest module:
```shell
python -m unittest
```

To run a specific test module:
```shell
python -m unittest tests.test_module
```

And to run a specific test within a module:
```shell
python -m unittest tests.test_module.TestClass.test_method
```

Using Pytest
If you prefer, you can use pytest to run the tests. Install it with pip:
```shell
pip install pytest
```

To run a specific test file:
```shell
pytest -v tests/unittests/test_bank_validators.py
```

And to run a specific test within a module:
```shell
pytest -v tests/unittests/test_bank_validators.py::TestBankValidators::test_yahav_validator
```

# License
This library is licensed under the MIT License.