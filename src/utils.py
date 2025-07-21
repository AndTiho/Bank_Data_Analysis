import json
import os
import urllib
from datetime import datetime
from typing import Any, Callable, ParamSpec, TypeVar

import pandas as pd
import requests
from dotenv import load_dotenv
from requests import HTTPError

T = TypeVar("T")
P = ParamSpec("P")
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
    try:
        url_x = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_list[0]}"
        url_y = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_list[1]}"
        payload: dict = {}
        headers = {"apikey": api_key_for_currency}
        response_x = requests.request("GET", url_x, headers=headers, data=payload)
        response_x.raise_for_status()
        result_x = response_x.json()
        response_y = requests.request("GET", url_y, headers=headers, data=payload)
        response_y.raise_for_status()
        result_y = response_y.json()

        if "rates" not in result_x or "rates" not in result_y:
            raise ValueError("Похоже вы исчерпали все бесплатные запросы.")
        return {
            currency_list[0]: result_x["rates"]["RUB"],
            currency_list[1]: result_y["rates"]["RUB"],
        }
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Ошибка подключения. Проверьте интернет-соединение")
    except requests.exceptions.HTTPError:
        raise HTTPError("HTTP ошибка. Проверьте URL или API ключ")
    except requests.exceptions.Timeout:
        raise TimeoutError("Превышено время ожидания. Проверьте интернет-соединение")
    except ValueError as e:
        raise ValueError(f"Ошибка: {e}")


def get_stocks_data(stocks_list: list) -> Any:
    """Функция принимает на вход список требуемых для поиска Акций и возвращает
    словарь в виде 'Акция': 'Стоимость'"""
    data = []
    result = {}
    try:
        for stock in stocks_list:
            url = f"https://financialmodelingprep.com/stable/quote-short?symbol={stock}&apikey={api_key_for_stocks}"
            response = urllib.request.urlopen(url)
            json_data = json.loads(response.read().decode("utf-8"))
            data.append(json_data[0])
        if not "symbol" or not "price":
            raise ValueError("Похоже вы исчерпали все бесплатные запросы")
        for i in data:
            result[i["symbol"]] = i["price"]
        return result

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return {}
    except KeyError as e:
        print(f"Ошибка в структуре ответа API: {e}")
        return {}


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


def excel_to_df(file_path: str) -> str | pd.DataFrame:
    """Функция принимает путь к файлу с данными Excel и возвращает DataFrame"""
    if not isinstance(file_path, str):
        return "Программе не передан файл с данными. Закрываем работу программы."
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        return "Программе не передан файл с данными. Закрываем работу программы."
    return df


def filter_by_date(df: str | pd.DataFrame, user_date: str) -> Any:
    """Функция принимает на вход дату и
    фильтрует DataFrame в диапазоне принимаемой даты с начал месяца этой самой даты блин
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Первый аргумент должен быть объектом pd.DataFrame")
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    end_date = pd.to_datetime(user_date)
    start_of_month = end_date.replace(day=1)
    return df[(df["Дата платежа"] >= start_of_month) & (df["Дата платежа"] <= end_date)]


def filter_by_date_three_month(df: str | pd.DataFrame, user_date: str) -> Any:
    """Функция принимает на вход дату и
    фильтрует DataFrame в диапазоне последние три месяца от принимаемой даты
    Дату вводить в формате YYYY-MM-DD
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Первый аргумент должен быть объектом pd.DataFrame")
    df_copy = df.copy()
    df_copy.loc[:, "Дата платежа"] = pd.to_datetime(df_copy["Дата платежа"], dayfirst=True)
    end_date = pd.to_datetime(user_date)
    start_date = end_date - pd.DateOffset(months=3)
    return df_copy[(df_copy["Дата платежа"] >= start_date) & (df_copy["Дата платежа"] <= end_date)]


def total_spent(df: str | pd.DataFrame) -> Any:
    """Функция принимает на вход DataFrame и с помощью pandas фильтрует по 'Статус': 'OK/Failed',
    фильтрует по тратам, группирует по 'Номер карты' и возвращает словарь, где
    ключ: Номер карты, значение: сумма всех трат по карте"""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Первый аргумент должен быть объектом pd.DataFrame")
    df_state = df[df["Статус"] == "OK"]
    df_negative = df_state[df_state["Сумма платежа"] < 0]
    card_name_grouped = df_negative.groupby("Номер карты")
    sum_price_by_card_number = card_name_grouped["Сумма платежа"].sum()
    total_spent_dict = sum_price_by_card_number.to_dict()
    return total_spent_dict


def top_transactions(df: str | pd.DataFrame) -> Any:
    """Функция принимает на вход DataFrame и с помощью pandas фильтрует по 'Статус': 'OK/Failed',
    фильтрует по тратам и возвращает словарь ТОП-5 транзакций по сумме платежа в DF"""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Первый аргумент должен быть объектом pd.DataFrame")
    df_state = df[df["Статус"] == "OK"]
    df_negative = df_state[df_state["Сумма платежа"] < 0]
    df_sort = df_negative.sort_values(by="Сумма платежа", ascending=True)
    df_sort_five = df_sort.head(5)
    top_five = df_sort_five.to_dict("records")
    return top_five


def group_by(df: str | pd.DataFrame) -> Any:
    """
    Функция для получения списка всех категорий из файла с транзакциями.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Первый аргумент должен быть объектом pd.DataFrame")
    return df["Категория"].dropna().unique().tolist()


def write_to_file(file_name: str) -> Callable[[Callable[P, str]], Callable[P, str]]:
    def writing(func: Callable[P, str]) -> Callable[P, str]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            result: str = func(*args, **kwargs)
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(result)
            return result

        return wrapper

    return writing


def excel_to_python_data(file_path: str) -> Any:
    """Функция принимает ПУТЬ к файлу EXCEL и преобразует его в Python список словарей,
    либо возвращает пустой Python список.
     Пример пути к файлу: './data/transactions_excel.xlsx'"""

    if not isinstance(file_path, str):
        print("'Путь к файлу' должен быть строкой. Возвращаем пустой список.")
        return []
    try:
        df = pd.read_excel(file_path)
        excel_data = df.to_dict("records")
    except OSError:
        print("Ошибка декодирования файла, возвращаем пустой список.")
        return []
    return list(excel_data)
