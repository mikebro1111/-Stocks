import requests
from bs4 import BeautifulSoup
import pymongo
import threading

from yahoo_client import YahooClient
from mongo_storage import MongoStorage
from prices import Prices


class WikiClient:
    @staticmethod
    def get_wiki_symbols():
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", {"class": "wikitable sortable"})
        symbols = [row.find_all("td")[0].text.strip() for row in table.find_all("tr")[1:]]
        return symbols


# Create a MongoDB manager class
class MongoDBManager:
    def init(self, db_url):
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client["stock_data"]
        self.collection = self.db["stock_prices"]

    def enter(self):
        return self

    def save_data(self, symbol, price):
        record = {"symbol": symbol, "price": price}
        self.collection.insert_one(record)

    def exit(self, exc_type, exc_val, exc_tb):
        self.client.close()


# Thread manager class
class ThreadManager:
    def init(self, symbols, db_url):
        self.symbols = symbols
        self.db_url = db_url
        self.storage = MongoStorage(self.db_url)

    def fetch_and_save(self, symbol):
        price = YahooClient.get_financial_data(symbol)
        if price:
            price_data = Prices(symbol=symbol, price=price)
            self.storage.save_one(price_data)

    def update_price(self, symbol, new_price):
        self.storage.update_one({"symbol": symbol}, {"price": new_price})

    def delete_symbol(self, symbol):
        self.storage.delete_one({"symbol": symbol})

    def execute_threads(self):
        threads = []
        for symbol in self.symbols:
            thread = threading.Thread(target=self.fetch_and_save, args=(symbol,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.update_price("AAPL", 155.0)
        self.delete_symbol("MSFT")

        found_prices = self.storage.find({})
        for price in found_prices:
            print(price)

        self.storage.close()
        