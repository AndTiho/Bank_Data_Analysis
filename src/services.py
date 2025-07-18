import datetime
import json

import pandas as pd


def cashback_bank(data: pd.DataFrame, year: int, month: int)->str:
    """Функция принимает на вход три аргумента: данные с транзакциями, год и месяц.
    На выходе мы получаем JSON-файл сколько на каждой категории заработано кэшбэка
    за выбранный месяц года"""
    year_month = datetime.date(year, month, 1)
    data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], dayfirst=True)
    filtered_data = data[
        data["Дата платежа"].dt.to_period("M")
        == f"{year_month.year}-{year_month.month}"
    ]
    df_state = filtered_data[filtered_data["Статус"] == "OK"]
    df_negative = df_state[df_state["Сумма платежа"] < 0]
    card_name_grouped = df_negative.groupby("Категория")
    sum_price_by_card_number = card_name_grouped["Бонусы (включая кэшбэк)"].sum()
    total_spent_dict = sum_price_by_card_number.to_dict()
    return json.dumps(total_spent_dict, ensure_ascii=False, indent=4)
