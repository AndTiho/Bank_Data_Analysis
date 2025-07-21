import logging
import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.abspath("."))

from src.reports import spending_by_category
from src.services import cashback_bank
from src.utils import PATH_TO_EXCEL, excel_to_df, excel_to_python_data, greetings, group_by
from src.views import main_website_page

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="./logs/reports.log",
    filemode="w",
    encoding="utf-8",
)

spending_by_category_logger = logging.getLogger("app.spending_by_category")
main_website_page_logger = logging.getLogger("app.main_website_page")
cashback_bank_logger = logging.getLogger("app.cashback_bank")


def main() -> str:
    """Функция для отображения всего функционала проекта Bank Analys Data(Bank_AD)"""

    # Приветствуем пользователя и просим выбрать какую часть реализуем в отвеет
    print(greetings())
    print(
        "Мы рады представить вам программу для работы с excel данными\n"
        "которая генерирует в ответ JSON данные для работы банковского приложения.\n"
        "Пожалуйста, введите номер пункта меню, по которому вы хотите получить ответ:\n"
        "1. Данные для главной страницы.\n"
        "2. Данные по выгодным категориям повышенного Кэшбэка.\n"
        "3. Данные трат по выбранной категории.\n"
        "4. Выход из программы."
    )
    user_input = input("...: ")
    while user_input not in ["1", "2", "3", "4"]:
        user_input = input("Введите пожалуйста корректный номер пункта: ")

    # Здесь отрабатываем функционал модуля views.py
    if user_input == "1":
        time.sleep(1)
        print(f"Вы выбрали пункт номер: {user_input}.")
        time.sleep(1)
        print("Вам необходимо ввести дату в формате YYYY-MM-DD HH:MM:SS.")
        time.sleep(1)
        print(
            "К сожалению в данный момент, для корректной работы необходимо выбрать дату"
            "находящуюся в представленном ниже диапазоне:\n"
            "01.01.2018 12:49:53 ---- 31.12.2021 16:44:00\n"
            "Вы можете скопировать дату для теста:\n"
            "2020-10-02 16:05:00\n"
            "Или же ввести exit для выхода из программы."
        )

        # В задании указано, что функция в views.py должна принимать на вход формат даты
        # YYYY-MM-DD HH:MM:SS --- так что тут мы обрабатываем корректность ввода
        while True:
            user_date = input("Ваша дата:   ")
            if user_date.lower() == "exit":
                time.sleep(1)
                print(f"Вы выбрали {user_date}...")
                time.sleep(1)
                print("Ну что ж...спасибо, что выбрали Bank_AD.")
                time.sleep(1)
                print("Мира вам и процветания -_^")
                sys.exit()
            try:
                # Пытаемся преобразовать строку в дату
                datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
                break  # Если успешно - выходим из цикла
            except ValueError:
                # Если возникла ошибка - просим ввести заново
                print("Неверный формат даты!")
                print("ПОЖАЛУЙСТА!!!!! введите дату в формате YYYY-MM-DD HH:MM:SS")

        # Здесь творим основную функцию из views.py и выводим результат со словами благодарности
        result = main_website_page(user_date)
        return result

    # Здесь отрабатываем функционал модуля services.py
    elif user_input == "2":
        time.sleep(1)
        print(f"Вы выбрали пункт номер: {user_input}.")
        time.sleep(1)
        print(
            "Чтобы определить наиболее выгодные категории Кэшбэка, необходимо указать "
            "интересующий вас год и месяц, а мы вам предоставим, какие категории были самыми выгодными"
            "в этот месяц заданного года."
        )
        time.sleep(1)
        print("Вам необходимо ввести дату в формате YYYY-MM")
        time.sleep(1)
        print(
            "К сожалению в данный момент, для корректной работы необходимо выбрать дату"
            "находящуюся в представленном ниже диапазоне:\n"
            "01.01.2018 12:49:53 ---- 31.12.2021 16:44:00\n"
            "Вы можете скопировать дату для теста:\n"
            "Год:2020-10\n"
            "Или же ввести exit для выхода из программы."
        )

        # В задании сказано, что функция должна принимать на вход параметры Year и Month
        # по этому тут мы отрабатываем вариант ввода пользователем корректных данных
        # для проверки работы основной функции из services.py
        while True:
            user_date = input("Ваша дата:   ")
            if user_date.lower() == "exit":
                time.sleep(1)
                print(f"Вы выбрали {user_date}...")
                time.sleep(1)
                print("Ну что ж...спасибо, что выбрали Bank_AD.")
                time.sleep(1)
                print("Мира вам и процветания -_^")
                sys.exit()
            try:
                date_parts = user_date.split("-")
                year = int(date_parts[0])
                month = int(date_parts[1])
                # Пытаемся преобразовать строку в дату
                datetime(year, month, day=1)
                break  # Если успешно - выходим из цикла
            except ValueError:
                # Если возникла ошибка - просим ввести заново
                print("Неверный формат даты!")
                print("ПОЖАЛУЙСТА!!!!! введите дату в формате YYYY-MM" " или введите exit для выхода")

        # Передаём в нашу функцию полученные параметры и тянем DataFrame через
        # заготовленную функцию из utils.py и кидаем туда же
        data = excel_to_python_data(PATH_TO_EXCEL)
        result = cashback_bank(data, year, month)

        return result

    # Тут работаем с функционалом из reports.py
    elif user_input == "3":
        df = excel_to_df(PATH_TO_EXCEL)
        time.sleep(1)
        print(f"Вы выбрали пункт номер: {user_input}.")
        time.sleep(1)
        print(
            "Что бы получить отчёт по тратам за последние три месяца по интересующей"
            'вас категории, вам для начала необходимо выбрать "Категорию".'
        )
        time.sleep(1)
        print(
            "Для корректной работы программы, просим вас выбрать категорию из тех,"
            "что предоставлены в файле с транзакциями\n"
            "Для теста рекомендуется скопировать: Аптеки"
        )
        time.sleep(1)
        print(f"{group_by(df)}")
        category = input("Ваша категория:").capitalize()

        # Выдаём список всех категорий и запрашиваем одну из них
        while category not in group_by(df):
            print(f"Выберете категорию из списка {group_by(df)}\n" f"или напишите exit для выхода.")
            category = input("Ваша категория:").capitalize()
            if category.lower() == "exit":
                time.sleep(1)
                print(f"Вы выбрали {category}...")
                time.sleep(1)
                print("Ну что ж...спасибо, что выбрали Bank_AD.")
                time.sleep(1)
                print("Мира вам и процветания -_^")
                sys.exit()
        time.sleep(1)

        # Запрос даты для сортировки "за последние 3 месяца от выбранной даты"
        print("Теперь Вам необходимо ввести дату в формате YYYY-MM-DD")
        time.sleep(1)
        print(
            "К сожалению в данный момент, для корректной работы необходимо выбрать дату"
            "находящуюся в представленном ниже диапазоне:\n"
            "01.01.2018 12:49:53 ---- 31.12.2021 16:44:00\n"
            "Вы можете скопировать дату для теста:\n"
            "Год:2020-10-20\n"
            "Или же ввести exit для выхода из программы."
        )
        while True:
            user_date = input("Ваша дата:   ")
            if user_date.lower() == "exit":
                time.sleep(1)
                print(f"Вы выбрали {user_date}...")
                time.sleep(1)
                print("Ну что ж...спасибо, что выбрали Bank_AD.")
                time.sleep(1)
                print("Мира вам и процветания -_^")
                sys.exit()

            # Тут выход если дата не выбрана, так как в функции в таком случае берётся нынешняя дата
            if not user_date:
                break
            try:
                # Пытаемся преобразовать строку в дату
                datetime.strptime(user_date, "%Y-%m-%d")
                break  # Если успешно - выходим из цикла
            except ValueError:
                # Если возникла ошибка - просим ввести заново
                print("Неверный формат даты!")
                print("ПОЖАЛУЙСТА!!!!! введите дату в формате YYYY-MM-DD" " или введите exit для выхода")

        result = spending_by_category(df, category, user_date)
        time.sleep(1)
        print('Напоминаем, что по заданию функция декорирована записью("w") результата в results.txt ')
        time.sleep(3)
        if result == "[]":
            print("К сожалению трат по выбранной категории в это время не было.")
        return result

    # Здесь отрабатывается вариант exit -> выход из программы
    else:
        time.sleep(1)
        print("Мы чувствуем, что вы выбрали пункт 4...")
        time.sleep(1)
        print("Ну что ж...спасибо, что выбрали Bank_AD.")
        time.sleep(1)
        return "Мира вам и процветания -_^"


###########

if __name__ == "__main__":

    print(main())

###########
