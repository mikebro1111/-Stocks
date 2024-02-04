import requests
from bs4 import BeautifulSoup
import pymongo

from src.core.yahoo_client import YahooClient
from src.core.database.mongo_storage import MongoStorage
from src.core.prices import Prices


class WikiClient:
    """A client for fetching stock symbols from Wikipedia."""

    @staticmethod
    def get_wiki_symbols(url):
        """Retrieve stock symbols from the given Wikipedia URL.

        Args:
            url (str): The Wikipedia URL to scrape for stock symbols.

        Returns:
            list: A list of stock symbols.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "wikitable sortable"})
        symbols = [row.find_all("td")[0].text.strip() for row in table.find_all("tr")[1:]]
        return symbols


class ThreadManager:
    """Manager class for handling threading operations."""

    def __init__(self, symbols, db_url):
        """Initialize the ThreadManager with symbols and a database URL.

        Args:
            symbols (list): A list of stock symbols.
            db_url (str): The database URL for MongoDB.
        """
        self.symbols = symbols
        self.db_url = db_url
        self.storage = MongoStorage(self.db_url)

    def fetch_and_save(self, symbol):
        """Fetch stock price and save it using MongoDB storage.

        Args:
            symbol (str): The stock symbol to fetch and save.
        """
        price = YahooClient.get_financial_data(symbol)
        if price:
            price_data = Prices(symbol=symbol, price=price)
            self.storage.save_one(price_data)

    def update_price(self, symbol, new_price):
        """Update the stock price for a given symbol.

        Args:
            symbol (str): The stock symbol to update.
            new_price (float): The new price to update.
        """
        self.storage.update_one({"symbol": symbol}, {"price": new_price})

    def delete_symbol(self, symbol):
        """Delete a stock symbol from storage.

        Args:
            symbol (str): The stock symbol to delete.
        """
        self.storage.delete_one({"symbol": symbol})
