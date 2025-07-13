import pandas as pd
from typing import Any
import os

PATH_TO_FILE = os.path.join(os.path.dirname(__file__), '../data', 'operations.xlsx')


def excel_to_python_data(file_path: str) -> Any:
    """Функция принимает ПУТЬ к файлу EXCEL и преобразует его в Python список словарей,
    либо возвращает пустой Python список.
     Пример пути к файлу: '../data/operations.xlsx'"""

    if not isinstance(file_path, str):
        print("'Путь к файлу' должен быть строкой. Возвращаем пустой список.")
        return []
    df = pd.read_excel(file_path)
    excel_data = df.to_dict("records")
    return list(excel_data)


# print(excel_to_python_data(PATH_TO_FILE)[0])