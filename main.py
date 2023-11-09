import requests
from bs4 import BeautifulSoup
import pymongo
import threading
import time


def get_financial_data(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.find('td', {'data-test': 'OPEN-value'})
        price = price_element.text if price_element else "Ціна не знайдена"

        return {
            "Ціна акцій": price
        }
    else:
        return None


def save_data_to_mongodb(symbol, collection):
    financial_data = get_financial_data(symbol)
    if financial_data:
        record = {
            "symbol": symbol,
            "price": financial_data["Ціна акцій"]
        }
        collection.insert_one(record)


def get_wiki():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"class": "wikitable sortable"})

    symbols = []

    for row in table.find_all("tr")[1:]:
        symbol = row.find_all("td")[0].text.strip()
        symbols.append(symbol)

    return symbols


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["stock_data"]
collection = db["stock_prices"]

symbols = get_wiki()

start_time = time.time()

threads = []

for symbol in symbols:
    thread = threading.Thread(target=save_data_to_mongodb, args=(symbol, collection))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()

execution_time = end_time - start_time
seconds = execution_time
minutes = seconds / 60

print("Час виконання програми в секундах:", seconds)
print("Час виконання програми в хвилинах:", minutes)

client.close()