import pytest

from src.utils import json_settings_for_currency, PATH_TO_JSON, json_settings_for_stocks


# json_settings_for_currency
def test_correct_work_currency():
    assert json_settings_for_currency(PATH_TO_JSON) == ['USD', 'EUR']

@pytest.mark.parametrize(
    "path, expected_result", [(0, []), ("", []), (1.5, []), ("not_a path", []), (None, []), ([], [])]
)
def test_all_errors_path_currency(path, expected_result):
    assert json_settings_for_currency(path) == expected_result

# json_settings_for_stocks

def test_correct_work_stocks():
    assert json_settings_for_stocks(PATH_TO_JSON) == ['AAPL', 'AMZN','GOOGL', 'MSFT', 'TSLA']

@pytest.mark.parametrize(
    "path, expected_result", [(0, []), ("", []), (1.5, []), ("not_a path", []), (None, []), ([], [])]
)
def test_all_errors_path_stocks(path, expected_result):
    assert json_settings_for_stocks(path) == expected_result