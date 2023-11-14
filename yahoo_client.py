import requests
from bs4 import BeautifulSoup


class YahooClient:
    @staticmethod
    def get_financial_data(symbol):
        url = f"https://finance.yahoo.com/quote/{symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.find('td', {'data-test': 'OPEN-value'})
            price = price_element.text if price_element else "Ціна не знайдена"
            return price
        else:
            return None
