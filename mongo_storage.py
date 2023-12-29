from pymongo import MongoClient
from prices import Prices
from typing import List, Optional


class MongoStorage:
    def init(self, db_url, db_name="stock_data", collection_name="stock_prices"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_one(self, price_data: Prices):
        return self.collection.insert_one(price_data.dict)

    def save_many(self, prices_data: List[Prices]):
        return self.collection.insert_many([price.dict for price in prices_data])

    def find(self, query: dict) -> List[Prices]:
        return [Prices(**data) for data in self.collection.find(query)]

    def aggregate(self, pipeline: list) -> List[Prices]:
        return [Prices(**data) for data in self.collection.aggregate(pipeline)]

    def update_one(self, filter: dict, update: dict) -> Optional[Prices]:
        result = self.collection.update_one(filter, {'$set': update})
        if result.matched_count:
            return self.find(filter)[0]
        return None

    def update_many(self, filter: dict, update: dict):
        return self.collection.update_many(filter, {'$set': update})

    def delete_one(self, filter: dict):
        return self.collection.delete_one(filter)

    def delete_many(self, filter: dict):
        return self.collection.delete_many(filter)

    def close(self):
        self.client.close()
