import datetime
import json
import logging
from typing import Optional

import pandas as pd

from src.utils import filter_by_date_three_month, write_to_file

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="./logs/reports.log",
    filemode="w",
    encoding="utf-8",
)

spending_by_category_logger = logging.getLogger("app.spending_by_category")


@write_to_file("./data/results.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция принимает данные транзакций, категорию на выбор пользователя и дату
    (по умолчанию берётся сегодняшняя) и возвращает траты по заданной категории за последние три месяца
    """
    spending_by_category_logger.info("Начало работы программы")
    # Если даты нет, создаём её сами черед datetime.now()
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        spending_by_category_logger.info(f"На вход не поступило даты. Взята текущая {date}")
    # Фильтруем по заданной дате за минусом трёх месяцев
    filtered_df = filter_by_date_three_month(transactions, date)
    # Фильтруем по заданной категории и возвращаем столбцу Дата платежа
    # тип - строка, а то JSON ругается.
    category_df = filtered_df[filtered_df["Категория"] == category]
    category_df.loc[:, "Дата платежа"] = category_df["Дата платежа"].astype(str)
    result = category_df.to_dict("records")

    spending_by_category_logger.info("Программа отработала корректно. Завершение работы")
    return json.dumps(result, ensure_ascii=False, indent=4)
