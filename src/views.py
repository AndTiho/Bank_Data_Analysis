import json

from src.utils import (
    PATH_TO_EXCEL,
    PATH_TO_JSON,
    excel_to_df,
    filter_by_date,
    get_currency,
    get_stocks_data,
    greetings,
    json_settings_for_currency,
    json_settings_for_stocks,
    top_transactions,
    total_spent,
)


def main_website_page(user_date):
    """
    Функция принимает на вход дату в формате YYYY-MM-DD HH:MM:SS и возвращает
    JSON-ответ со следующими данными:
    1. Приветствие;
    2. По каждой карте:
      -последние 4 цифры карты;
      -общая сумма расходов;
      -кешбэк (1 рубль на каждые 100 рублей).
    3. Топ-5 транзакций по сумме платежа.
    4. Курс валют.
    5. Стоимость акций из S&P500.
    """

    # Получаем DataFrame и фильтруем по входящей дате
    df = excel_to_df(PATH_TO_EXCEL)
    filtered_df = filter_by_date(df, user_date)

    # Пункт 2. Работаем над строкой для JSON-ответа суммы трат по основным картам по заданному датой месяцу
    result_total_spent = total_spent(filtered_df)
    total_spent_for_json = {}
    for key, value in result_total_spent.items():
        total_spent_for_json = {
            "last_digits": key[-4:],
            "total_spent": round(-value, 2),
            "cashback": round((-value / 100), 2),
        }

    # Пункт 3. Работаем над JSON-ответ по пункту ТОП-5 трат
    result_top_five = top_transactions(filtered_df)
    top_five_json = []
    for i in result_top_five:
        top_five_json.append(
            {
                "date": i.get("Дата операции")[:10],
                "amount": i.get("Сумма операции с округлением"),
                "category": i.get("Категория"),
                "description": i.get("Описание"),
            }
        )

    # Пункт 4. Работаем для JSON над курсом валют
    currency = get_currency(json_settings_for_currency(PATH_TO_JSON))
    currency_json = []
    for key, value in currency.items():
        currency_json.append({"currency": key, "rate": value})

    # Пункт 5. Работаем для JSON над курсом акций
    stocks = get_stocks_data(json_settings_for_stocks(PATH_TO_JSON))
    stocks_json = []
    for key, value in stocks.items():
        stocks_json.append({"stock": key, "price": value})

    return json.dumps(
        {
            "greeting": greetings(),
            "cards": [total_spent_for_json],
            "top_transactions": top_five_json,
            "currency_rates": currency_json,
            "stock_prices": stocks_json,
        },
        ensure_ascii=False,
        indent=4,
    )

