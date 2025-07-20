import json
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import (PATH_TO_EXCEL, PATH_TO_JSON, excel_to_df, filter_by_date, filter_by_date_three_month,
                       get_currency, get_stocks_data, greetings, group_by, json_settings_for_currency,
                       json_settings_for_stocks, top_transactions, total_spent, write_to_file)

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


def test_get_currency():
    with patch("requests.request") as mock_req:
        # Создаем два разных ответа
        response_x = MagicMock()
        response_x.json.return_value = {
            "base": "USD",
            "date": "2021-03-17",
            "rates": {"RUB": 90},
            "success": True,
            "timestamp": 100,
        }

        response_y = MagicMock()
        response_y.json.return_value = {
            "base": "EUR",
            "date": "2021-03-17",
            "rates": {"RUB": 100},
            "success": True,
            "timestamp": 150,
        }

        mock_req.side_effect = [response_x, response_y]

        assert get_currency(["USD", "EUR"]) == {"USD": 90, "EUR": 100}


# Тесты для get_stocks_data - получение курса Акций с API


def test_get_stocks_data_correct_work():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response_aapl = MagicMock()
        mock_response_aapl.read.return_value = json.dumps([{"symbol": "AAPL", "price": 150.0}]).encode("utf-8")

        mock_response_googl = MagicMock()
        mock_response_googl.read.return_value = json.dumps([{"symbol": "GOOGL", "price": 2800.0}]).encode("utf-8")

        mock_urlopen.side_effect = [mock_response_aapl, mock_response_googl]

        assert get_stocks_data(["AAPL", "GOOGL"]) == {"AAPL": 150.0, "GOOGL": 2800.0}


# greetings - простое приветствие по текущей дате/времени


@pytest.mark.parametrize(
    "hour, expected_result",
    [
        (1, "Доброй ночи"),
        (5, "Доброе утро"),
        (10, "Доброе утро"),
        (11, "Добрый день"),
        (15, "Добрый день"),
        (16, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
    ],
)
def test_greetings_correct_work(hour, expected_result):
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 7, 19, hour)
        assert greetings() == expected_result


# excel_to_df - получаем DataFrame из excel данных
def test_excel_to_df():
    df = excel_to_df(PATH_TO_EXCEL)
    assert len(df.columns) == 15


def test_excel_no_path():
    assert excel_to_df("") == "Программе не передан файл с данными. Закрываем работу программы."


def test_excel_not_str():
    assert excel_to_df(1) == "Программе не передан файл с данными. Закрываем работу программы."


# filter_by_date - фильтруем DataFrame по дате


def test_filter_by_date_correct_work(my_dataframe):
    expected_df = pd.DataFrame({"Дата платежа": pd.to_datetime(["2020-01-01"]), "state": ["EXECUTED"]})
    filtered_df = filter_by_date(my_dataframe, "2020-01-01")
    assert filtered_df.equals(expected_df)


def test_filter_by_date_out_of_date(my_dataframe):
    filtered_df = filter_by_date(my_dataframe, "2025-01-01")
    assert filtered_df.empty


def test_filter_by_date_type_check():
    user_date = "2020-01-01"
    with pytest.raises(TypeError):
        filter_by_date("не DataFrame", user_date)


# filter_by_date_three_month - фильтруем данные по дате и преследующих  3х месяцев


def test_filter_by_date_three_month_correct_work():
    df = excel_to_df(PATH_TO_EXCEL)
    df_copy = df.copy()
    df_copy.loc[:, "Дата платежа"] = pd.to_datetime(df_copy["Дата платежа"], dayfirst=True)
    end_date = pd.to_datetime("2020-10-02")
    start_date = end_date - pd.DateOffset(months=3)
    expected_df = df_copy[(df_copy["Дата платежа"] >= start_date) & (df_copy["Дата платежа"] <= end_date)]
    filtered_df = filter_by_date_three_month(df, "2020-10-02")

    assert filtered_df.equals(expected_df)


def test_filter_by_date_three_month_out_of_date(my_dataframe):
    filtered_df = filter_by_date_three_month(my_dataframe, "2025-01-01")
    assert filtered_df.empty


def test_filter_by_date_three_month_type_check():
    user_date = "2020-01-01"
    with pytest.raises(TypeError):
        filter_by_date_three_month("не DataFrame", user_date)


# total_spent - сумма всех трат


def test_total_spent_correct_work():
    df = excel_to_df(PATH_TO_EXCEL)
    assert total_spent(df) == {"*4556": -1017972.02, "*5091": -17367.5, "*7197": -2478419.56}


def test_total_spent_type_check():
    with pytest.raises(TypeError):
        total_spent("не DataFrame")


# top_transactions - топ 5 транзакций
def test_top_transactions_correct_work():
    df = excel_to_df(PATH_TO_EXCEL)
    filtered_df = filter_by_date(df, "2020-10-02")
    result1 = top_transactions(filtered_df.copy())
    result2 = top_transactions(filtered_df.copy())

    df1 = pd.DataFrame(result1)
    df2 = pd.DataFrame(result2)

    pd.testing.assert_frame_equal(df1, df2)


def test_top_transactions_type_check():
    with pytest.raises(TypeError):
        top_transactions("не DataFrame")


# group_by - получает список всех Категорий в DataFrame


def test_group_by(my_category_list):
    df = excel_to_df(PATH_TO_EXCEL)
    print(group_by(df))
    assert group_by(df) == my_category_list


def test_group_by_type_check():
    with pytest.raises(TypeError):
        group_by("не DataFrame")


# write_to_file - декоратор записи в файл


def test_basic_functionality():
    # Создаём временный файл с корректным управлением ресурсами
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8", suffix=".txt") as temp_file:
        file_path = temp_file.name

        @write_to_file(file_path)
        def test_func():
            return "Test string"

        result = test_func()
        assert result == "Test string", "Ошибка в возвращаемом значении"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == "Test string", "Ошибка в содержимом файла"
