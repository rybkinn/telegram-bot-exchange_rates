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
    r = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
    src = bs(r.content, "lxml")
    for valute_type, parameters in VALUTE_INFO.items():
        price = str(src.find("valute", id=parameters['id']).find("value"))[7:-8]
        parsed_information += f"{valute_type} = <b>{price}</b> ({parameters['description']})\n"
    return parsed_information


def parce_cryptocurrency(cryptocurrencies: tuple, towards: tuple) -> str:
    """
    Accepts the types of cryptocurrencies and the types of currencies 
    to be brought to. Returns the current course.
    Site api - https://min-api.cryptocompare.com.
    """

    CRIPTOVALUTE_INFO = {
        "BTC": "Bitcoin",
        "ETH": "Ethereum"
    }

    towards_string = ",".join(towards)
    parsed_information = str()
    for crypto_type in cryptocurrencies:
        compiled_link = \
        f"https://min-api.cryptocompare.com/data/price?fsym={crypto_type}&tsyms={towards_string}"
        r = requests.get(compiled_link)
        parsed_information += f"{CRIPTOVALUTE_INFO[crypto_type]}:\n"
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
            parsed_information += f"    {towards_type} = <b>{price}</b> \n"
        parsed_information += "\n"
    return parsed_information
