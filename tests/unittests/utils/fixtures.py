import pytest


@pytest.fixture
def bank_account(request):
    return request.param
