from utils import PATH_TO_EXCEL, excel_to_df, filter_by_date

df = excel_to_df(PATH_TO_EXCEL)
test_df = df.sample(1000)
test_data = '2020-10-02'

print(filter_by_date(test_df, test_data))