import requests
from bs4 import BeautifulSoup


class YahooClient:
    """
    A client for fetching financial data from Yahoo Finance.
    """

    @staticmethod
    def get_financial_data(symbol, url):
        """
        Retrieve the financial data for a given stock symbol from Yahoo Finance.

        Args:
            symbol (str): The stock symbol for which financial data is being requested.
            url (str): The URL to fetch the financial data from Yahoo Finance.

        Returns:
            str: The price of the stock if found, otherwise a message indicating the price is not found, or None if the request fails.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.find('td', {'data-test': 'OPEN-value'})
            price = price_element.text if price_element else "Ціна не знайдена"
            return price
        else:
            return None
