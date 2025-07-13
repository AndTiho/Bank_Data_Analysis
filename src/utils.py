import json

import pandas as pd
from typing import Any
import os
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

PATH_TO_EXCEL = os.path.join(os.path.dirname(__file__), '../data', 'operations.xlsx')
PATH_TO_JSON = os.path.join(os.path.dirname(__file__), '../user_settings.json')

def json_settings_for_currency(file_path: str) -> Any:
    """Функция принимает ПУТЬ к файлу JSON и преобразует его в Python список возвращая значения требуемых валют
    из файла настроек user_settings.json"""
    with open(file_path, "r", encoding="utf-8") as file:
        python_data = json.load(file)
        currency_list  = python_data.get('user_currencies')
    return currency_list

def json_settings_for_stocks(file_path: str) -> Any:
    """Функция принимает ПУТЬ к файлу JSON и преобразует его в Python список возвращая значения требуемых акций
    из файла настроек user_settings.json"""
    with open(file_path, "r", encoding="utf-8") as file:
        python_data = json.load(file)
        stocks_list  = python_data.get('user_currencies')
    return stocks_list


def get_currency(currency_list):
    """Функция принимает на вход список из двух валют требуемых для нахождения курсов с apilayer.com
     и возвращает словарь 'Валюта: курс в рублях' """
    url_x = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_list[0]}"
    url_y = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency_list[1]}"
    payload = {}
    headers = {
        "apikey": api_key
    }
    response_x = requests.request("GET", url_x, headers=headers, data=payload)
    result_x = response_x.json()
    response_y = requests.request("GET", url_y, headers=headers, data=payload)
    result_y = response_y.json()

    return {currency_list[0]:result_x['rates']['RUB'], currency_list[1]:result_y['rates']['RUB']}

print(get_currency(json_settings_for_currency(PATH_TO_JSON)))


def greetings(date: str)->str:
    """Функция принимает на вход Дату в виде строки, преобразует в объект времени
    и возвращает """
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if 5 <= date_object.hour < 11:
        return 'Доброе утро'
    elif 11 <= date_object.hour < 16:
        return 'Добрый день'
    elif 16 <= date_object.hour < 23:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


def excel_to_df(file_path: str):
    """Функция принимает путь к файлу с данными Excel и возвращает DataFrame"""
    df = pd.read_excel(file_path)
    return df


def filter_by_date(df, end_date: str)-> Any:
    """Функция принимает на вход дату и
    фильтрует DataFrame в диапазоне принимаемой даты с начал месяца этой самой даты блин"""
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True)
    end_date = pd.to_datetime(end_date)
    start_of_month = end_date.replace(day=1)
    return df[(df['Дата платежа'] >= start_of_month) &
              (df['Дата платежа'] <= end_date)]


def total_spent(df) -> Any:
    """Функция принимает на вход Excel файл и с помощью pandas фильтрует по 'Статус': 'OK/Failed',
     фильтрует по тратам, группирует по 'Номер карты' и возвращает словарь, где
     ключ: номер карты, значение: сумма всех расходов"""
    df = pd.read_excel(df)
    df_state = df[df['Статус'] == 'OK']
    df_negative = df_state[df_state['Сумма платежа'] < 0]
    card_name_grouped = df_negative.groupby('Номер карты')
    sum_price_by_card_number = card_name_grouped['Сумма платежа'].sum()
    total_spent_dict = sum_price_by_card_number.to_dict()
    return total_spent_dict

def last_four_card_numbers(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает последние 4 цифры номера """
    return card_number[-4:]





# def excel_to_python_data(file_path: str) -> Any:
#     """Функция принимает ПУТЬ к файлу EXCEL и преобразует его в Python список словарей,
#     либо возвращает пустой Python список.
#      Пример пути к файлу: '../data/operations.xlsx'"""
#
#     if not isinstance(file_path, str):
#         print("'Путь к файлу' должен быть строкой. Возвращаем пустой список.")
#         return []
#     try:
#         df = pd.read_excel(file_path)
#         excel_data = df.to_dict("records")
#     except OSError:
#         print("Ошибка декодирования файла, возвращаем пустой список.")
#         return []
#     return list(excel_data)