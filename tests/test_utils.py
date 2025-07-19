from unittest.mock import patch

import pytest

from src.utils import (PATH_TO_JSON, greetings, json_settings_for_currency,
                       json_settings_for_stocks)

# Тесты для json_settings_for_currency - использует JSON настройки для получения нужных валют


def test_correct_work_currency():
    assert json_settings_for_currency(PATH_TO_JSON) == ["USD", "EUR"]


@pytest.mark.parametrize(
    "path, expected_result",
    [(0, []), ("", []), (1.5, []), ("not_a path", []), (None, []), ([], [])],
)
def test_all_errors_path_currency(path, expected_result):
    assert json_settings_for_currency(path) == expected_result


# Тесты для json_settings_for_stocks - использует JSON настройки для получения списка требуемых акций


def test_correct_work_stocks():
    assert json_settings_for_stocks(PATH_TO_JSON) == [
        "AAPL",
        "AMZN",
        "GOOGL",
        "MSFT",
        "TSLA",
    ]


@pytest.mark.parametrize(
    "path, expected_result",
    [(0, []), ("", []), (1.5, []), ("not_a path", []), (None, []), ([], [])],
)
def test_all_errors_path_stocks(path, expected_result):
    assert json_settings_for_stocks(path) == expected_result


# Тесты для get_currency - получения курса валют с API

# Тесты для get_stocks_data - получение курса Акций с API

# greetings - простое приветствие по текущей дате/времени


def test_greetings_correct_work():
    with patch("datetime.now", return_value="23.59.59"):
        assert greetings() == "Добрый день"


# excel_to_df - получаем DataFrame из excel данных

# filter_by_date - фильтруем DataFrame по дате

# filter_by_date_three_month - фильтруем данные по дате и преследующих  3х месяцев

# total_spent - сумма всех трат

# top_transactions - топ 5 транзакций

# group_by - получает список всех Категорий в DataFrame

# write_to_file - декоратор записи в файл
