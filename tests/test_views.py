import json

from src.views import main_website_page


def test_views():

    result = main_website_page("2020-10-02 19:45:02")
    data = json.loads(result)

    assert 1655 <= len(main_website_page("2020-10-25 19:45:02")) <= 1660
    assert data["greeting"] == "Доброе утро"
    assert len(data["cards"]) == 1
    assert data["cards"][0]["last_digits"] == "7197"
    assert data["stock_prices"][1]["stock"] == "AMZN"
