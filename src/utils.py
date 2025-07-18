import json
import os
import urllib
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
api_key_for_currency = os.getenv("API_KEY_for_currency")
api_key_for_stocks = os.getenv("API_KEY_for_stocks")

PATH_TO_EXCEL = os.path.join(os.path.dirname(__file__), "../data", "operations.xlsx")
PATH_TO_JSON = os.path.join(os.path.dirname(__file__), "../user_settings.json")


def json_settings_for_currency(file_path: str) -> Any:
    """Функция принимает ПУТЬ к файлу JSON и преобразует его в Python список возвращая значения требуемых валют
    из файла настроек user_settings.json"""
    if not isinstance(file_path, str):
        print("'Путь к файлу' должен быть строкой. Возвращаем пустой список.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            python_data = json.load(file)
            currency_list = python_data.get("user_currencies")
    except OSError:
        print("Ошибка декодирования файла, возвращаем пустой список.")
        return []
    return currency_list


def json_settings_for_stocks(file_path: str) -> Any:
    """Функция принимает ПУТЬ к файлу JSON и преобразует его в Python список возвращая значения требуемых акций
    из файла настроек user_settings.json"""
    if not isinstance(file_path, str):
        print("'Путь к файлу' должен быть строкой. Возвращаем пустой список.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            python_data = json.load(file)
            stocks_list = python_data.get("user_stocks")
    except OSError:
        print("Ошибка декодирования файла, возвращаем пустой список.")
        return []
    return stocks_list


def get_currency(currency_list: list) -> Any:
    """Функция принимает на вход список из двух валют требуемых для нахождения курсов с apilayer.com
    и возвращает словарь 'Валюта: курс в рублях'"""
    url_x = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_list[0]}"
    url_y = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_list[1]}"
    payload: dict = {}
    headers = {"apikey": api_key_for_currency}
    response_x = requests.request("GET", url_x, headers=headers, data=payload)
    result_x = response_x.json()
    response_y = requests.request("GET", url_y, headers=headers, data=payload)
    result_y = response_y.json()

    return {
        currency_list[0]: result_x["rates"]["RUB"],
        currency_list[1]: result_y["rates"]["RUB"],
    }


def get_stocks_data(stocks_list: list) -> Any:
    """Функция принимает на вход список требуемых для поиска Акций и возвращает
    словарь в виде 'Акция': 'Стоимость'"""
    data = []
    result = {}
    for stock in stocks_list:
        url = f"https://financialmodelingprep.com/stable/quote-short?symbol={stock}&apikey={api_key_for_stocks}"
        response = urllib.request.urlopen(url)
        json_data = json.loads(response.read().decode("utf-8"))
        data.append(json_data[0])
    for i in data:
        result[i["symbol"]] = i["price"]
    return result


def greetings() -> str:
    """Функция определяет текущее время и приветствует героя
    по всем правилам этикета времени"""
    date_object = datetime.now()
    if 5 <= date_object.hour < 11:
        return "Доброе утро"
    elif 11 <= date_object.hour < 16:
        return "Добрый день"
    elif 16 <= date_object.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def excel_to_df(file_path: str) -> pd.DataFrame:
    """Функция принимает путь к файлу с данными Excel и возвращает DataFrame"""
    df = pd.read_excel(file_path)
    return df


def filter_by_date(df: pd.DataFrame, user_date: str) -> pd.DataFrame:
    """Функция принимает на вход дату и
    фильтрует DataFrame в диапазоне принимаемой даты с начал месяца этой самой даты блин
    """
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    end_date = pd.to_datetime(user_date)
    start_of_month = end_date.replace(day=1)
    return df[(df["Дата платежа"] >= start_of_month) & (df["Дата платежа"] <= end_date)]


def filter_by_date_three_month(df: pd.DataFrame, user_date: str) -> Any:
    """Функция принимает на вход дату и
    фильтрует DataFrame в диапазоне последние три месяца от принимаемой даты
    Дату вводить в формате YYYY-MM-DD
    """
    df_copy = df.copy()
    df_copy.loc[:, "Дата платежа"] = pd.to_datetime(
        df_copy["Дата платежа"], dayfirst=True
    )
    end_date = pd.to_datetime(user_date)
    start_date = end_date - pd.DateOffset(months=3)
    return df_copy[
        (df_copy["Дата платежа"] >= start_date) & (df_copy["Дата платежа"] <= end_date)
    ]


def total_spent(df: pd.DataFrame) -> Any:
    """Функция принимает на вход DataFrame и с помощью pandas фильтрует по 'Статус': 'OK/Failed',
    фильтрует по тратам, группирует по 'Номер карты' и возвращает словарь, где
    ключ: Номер карты, значение: сумма всех трат по карте"""
    df_state = df[df["Статус"] == "OK"]
    df_negative = df_state[df_state["Сумма платежа"] < 0]
    card_name_grouped = df_negative.groupby("Номер карты")
    sum_price_by_card_number = card_name_grouped["Сумма платежа"].sum()
    total_spent_dict = sum_price_by_card_number.to_dict()
    return total_spent_dict


def top_transactions(df: pd.DataFrame) -> Any:
    """Функция принимает на вход DataFrame и с помощью pandas фильтрует по 'Статус': 'OK/Failed',
    фильтрует по тратам и возвращает словарь ТОП-5 транзакций по сумме платежа в DF"""
    df_state = df[df["Статус"] == "OK"]
    df_negative = df_state[df_state["Сумма платежа"] < 0]
    df_sort = df_negative.sort_values(by="Сумма платежа", ascending=True)
    df_sort_five = df_sort.head(5)
    top_five = df_sort_five.to_dict("records")
    return top_five


def group_by(df: pd.DataFrame) -> pd.DataFrame:
    """
    Функция для получения списка всех категорий из файла с транзакциями.
    """
    return df["Категория"].dropna().unique().tolist()


def write_to_file(file_name):
    def writing(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(result)
            return result

        return wrapper

    return writing
