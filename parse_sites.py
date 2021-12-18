# Parse site https://www.cbr.ru/scripts/XML_daily.asp
import requests

import emoji
from bs4 import BeautifulSoup as bs


def parse_monetary_currency() -> str:
    """
    Parses the xml site https://www.cbr.ru/scripts/XML_daily.asp 
    and returns the rate for the current date.
    """
    
    VALUTE_INFO = {
        "USD": {
            "id": "R01235",
            "description": "Доллар США",
            "emoji": ":us:"
        },
        "EUR": {
            "id": "R01239",
            "description": "Евро",
            "emoji": ":us:"
        },
        "UAH": {
            "id": "R01720",
            "description": "Украинских гривен"
        }
    }

    parsed_information = str()

    # r = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
    # html = bs(r.content, "lxml")

    with open("test_cbr.xml", "r") as xml_file:
        src = bs(xml_file.read(), 'lxml')
        for valute_type, parameters in VALUTE_INFO.items():
            price = str(src.find("valute", id=parameters['id']).find("value"))[7:-8]
            parsed_information += f"{valute_type} = {price} ({parameters['description']})"
    
    return parsed_information


def parce_cryptocurrency(cryptocurrencies: tuple, towards: tuple) -> str:
    """
    Some description.
    """

    towards_string = ",".join(towards)
    parsed_information = str()
    for crypto_type in cryptocurrencies:
        compiled_link = \
        f"https://min-api.cryptocompare.com/data/price?fsym={crypto_type}&tsyms={towards_string}"
        r = requests.get(compiled_link)
        for towards_type in towards:
            price = str(r.json()[towards_type])
            remainder = None
            if "." in price:
                temp_price, remainder = price.split(".")
            else:
                temp_price = price
            price = '{0:,}'.format(int(temp_price)).replace(',', ' ')
            if remainder is not None:
                price = price + "." + remainder
            parsed_information += f"{crypto_type}-{towards_type} = {price} \n"
        parsed_information += "\n"
    return parsed_information
