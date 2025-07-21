import json
from datetime import datetime

import pandas as pd

from src.reports import spending_by_category
from src.utils import PATH_TO_EXCEL, excel_to_df


def test_reports():
    df = excel_to_df(PATH_TO_EXCEL)
    result = spending_by_category(df, "Аптеки", date="2020-10-02")
    data = json.loads(result)

    assert len(data) == 6
    assert data[0]["Сумма платежа"] == -514.0
    assert data[2]["Кэшбэк"] == 13.0


def test_reports_date():
    df = excel_to_df(PATH_TO_EXCEL)
    result = spending_by_category(df, "Аптеки", date="2020-10-02")
    data = json.loads(result)

    end_date = datetime.strptime("2020-10-02", "%Y-%m-%d")
    start_date = end_date - pd.DateOffset(months=3)

    first_payment_date = datetime.strptime(data[0]["Дата платежа"], "%Y-%m-%d %H:%M:%S")
    last_payment_date = datetime.strptime(data[-1]["Дата платежа"], "%Y-%m-%d %H:%M:%S")

    assert start_date <= first_payment_date <= end_date
    assert start_date <= last_payment_date <= end_date


def test_no_data():
    df = excel_to_df(PATH_TO_EXCEL)
    result = spending_by_category(df, "Аптеки", date=None)
    data = json.loads(result)

    assert data == []
