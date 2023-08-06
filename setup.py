from setuptools import find_packages
from setuptools import setup

setup(
    name='israel-bank-account-validator',
    version='1.0.0',
    description='Validation for israel bank account numbers',
    author='Kirill Goldshtein',
    author_email='kirill@cellosign.com',
    packages=find_packages(),
    python_requires='>=3.9',
)
