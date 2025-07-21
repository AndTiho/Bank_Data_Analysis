import json
import logging
import math
from collections import Counter
from typing import Counter as CounterType
from typing import List

cashback_bank_logger = logging.getLogger("app.cashback_bank")


def cashback_bank(data: List, year: int, month: int) -> str:
    """Функция принимает на вход три аргумента: данные с транзакциями, год и месяц.
    На выходе мы получаем JSON-файл сколько на каждой категории заработано кэшбэка
    за выбранный месяц года"""
    cashback_bank_logger.info("Начало работы программы")

    if not isinstance(data, list):
        print("Данные должны быть списком словарей. Возвращаем пустой список.")
        cashback_bank_logger.warning("Данные должны быть списком словарей. Завершаем работу программы")
        return json.dumps([])
    year = int(year) if isinstance(year, str) else year
    month = int(month) if isinstance(month, str) else month

    new_list = [i for i in data if f"{month}.{year}" in str(i["Дата платежа"])]
    cashback_counter: CounterType[str] = Counter()
    for item in new_list:
        if item["Кэшбэк"] is not None and not math.isnan(item["Кэшбэк"]):
            cashback_counter[item["Категория"]] += item["Кэшбэк"]

    cashback_bank_logger.info("Программа отработала корректно. Завершение работы")
    return json.dumps(cashback_counter, ensure_ascii=False, indent=4, sort_keys=True)
