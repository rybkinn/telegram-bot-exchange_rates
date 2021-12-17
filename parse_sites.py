# Parse site https://www.cbr.ru/scripts/XML_daily.asp
import requests
from bs4 import BeautifulSoup as bs


def parse_monetary_currency() -> str:
    """
    Parses the xml site https://www.cbr.ru/scripts/XML_daily.asp 
    and returns the rate for the current date.
    """
    
    VALUTE_INFO = {
        "USD": {
            "id": "R01235",
            "description": "Доллар США"
        },
        "EUR": {
            "id": "R01239",
            "description": "Евро"
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
            parsed_information += f"{valute_type} = {price} ({parameters['description']})\n"
    
    return parsed_information


def parce_cryptocurrency(cryptocurrencies: tuple, towards: tuple) -> str:
    """
    Some description.
    """
    CRYPTOCURRENCIES_INFO = {
        "BTC": "Bitcoin",
        "ETH": "Ethereum"
    }

    towards_string = ",".join(towards)
    parsed_information = str()
    for crypto_type in cryptocurrencies:
        compiled_link = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_type}&tsyms={towards_string}"
        r = requests.get(compiled_link)
        for towards_type in towards:
            if towards_type == towards[0]:
                parsed_information += f"{CRYPTOCURRENCIES_INFO[crypto_type]} - {r.json()[towards_type]} {towards_type}\n"
                current_space = parsed_information.index("-") + 2
            else:
                parsed_information += (" " * current_space) + f"{r.json()[towards_type]} {towards_type}\n"
    return parsed_information
