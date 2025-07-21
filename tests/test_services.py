import json

import pytest

from src.services import cashback_bank
from src.utils import PATH_TO_EXCEL, excel_to_python_data


def test_services():
    date = excel_to_python_data(PATH_TO_EXCEL)
    data = json.loads(cashback_bank(date, 2020, 2))

    assert data == {"Аптеки": 303.0, "Ж/д билеты": 80.0, "Кино": 4.0, "Транспорт": 6.0, "Фастфуд": 0.0}


@pytest.mark.parametrize(
    "path, expected_result", [(0, "[]"), ("", "[]"), (1.5, "[]"), ("not_a path", "[]"), (None, "[]"), ([], "{}")]
)
def test_cashback_bank_data_not_list(path, expected_result):
    assert cashback_bank(path, 2020, 2) == expected_result


def test_cashback_bank_data_str():
    date = excel_to_python_data(PATH_TO_EXCEL)
    data = json.loads(cashback_bank(date, "2020", "2"))

    assert data == {"Аптеки": 303.0, "Ж/д билеты": 80.0, "Кино": 4.0, "Транспорт": 6.0, "Фастфуд": 0.0}
