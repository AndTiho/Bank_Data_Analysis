import datetime
import json
from typing import Optional

import pandas as pd

from src.utils import filter_by_date_three_month, write_to_file


@write_to_file("./data/results.txt")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> str:
    """Функция принимает данные транзакций, категорию на выбор пользователя и дату
    (по умолчанию берётся сегодняшняя) и возвращает траты по заданной категории за последние три месяца
    """
    # Если даты нет, создаём её сами черед datetime.now()
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    # Фильтруем по заданной дате за минусом трёх месяцев
    filtered_df = filter_by_date_three_month(transactions, date)
    # Фильтруем по заданной категории и возвращаем столбцу Дата платежа
    # тип - строка, а то JSON ругается.
    category_df = filtered_df[filtered_df["Категория"] == category]
    category_df.loc[:, "Дата платежа"] = category_df["Дата платежа"].astype(str)
    result = category_df.to_dict("records")

    # Возвращаем JSON
    return json.dumps(result, ensure_ascii=False, indent=4)
