import pytest
from src.utils import excel_to_python_data
import pandas as pd
from unittest.mock import mock_open, patch

@pytest.mark.parametrize(
    "path, expected_result", [(0, []), ("", []), (1.5, []), ("not_a path", []), (None, []), ([], [])]
)
def test_all_errors_excel(path, expected_result):
    assert excel_to_python_data(path) == expected_result


# my_list взят из conftest.py
def test_excel_to_python_data(my_list):
    mock_df = pd.DataFrame(my_list)
    with patch("pandas.read_excel", return_value=mock_df):
        result = excel_to_python_data("any_path")
        assert result == my_list
