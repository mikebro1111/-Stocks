from pymongo import MongoClient
from src.core.database.base_storage import BaseStorage


class MongoStorage(BaseStorage):
    """
    MongoStorage is a concrete implementation of the BaseStorage abstract class,
    providing MongoDB specific storage operations.

    Attributes:
        client (MongoClient): The client instance for MongoDB operations.
        db (Database): The specific database in MongoDB.
        collection (Collection): The specific collection in the database for operations.
    """

    def __init__(self, db_url, db_name="stock_data", collection_name="stock_prices"):
        """
        Initialize a new instance of MongoStorage.

        Args:
            db_url (str): The URL for the MongoDB database.
            db_name (str, optional): The name of the database. Defaults to "stock_data".
            collection_name (str, optional): The name of the collection. Defaults to "stock_prices".
        """
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def close(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()
