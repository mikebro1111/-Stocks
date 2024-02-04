import importlib
import pymongo


class MongoDBManager:
    """Manager class for MongoDB operations."""

    def __init__(self, db_url):
        """Initialize the MongoDB client.

        Args:
            db_url (str): The MongoDB connection URL.
        """
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client["stock_data"]
        self.collection = self.db["stock_prices"]

    def save_data(self, symbol, price):
        """Save stock data into the MongoDB collection.

        Args:
            symbol (str): The stock symbol.
            price (float): The stock price.
        """
        record = {"symbol": symbol, "price": price}
        self.collection.insert_one(record)

    def close(self):
        """Exit the runtime context and close the MongoDB client."""
        self.client.close()

def get_storage_class(settings):
    """Dynamically load and return the storage class based on settings."""
    module_name, class_name = settings['STORAGE_CLASS'].rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

# Example usage
settings = {
    'STORAGE_CLASS': 'path.to.MongoDBManager', # Replace 'path.to' with the actual module path
    'DB_URL': 'your_mongodb_url'
}

# Dynamically load the storage class
StorageClass = get_storage_class(settings)
storage_manager = StorageClass(settings['DB_URL'])

# Use the storage manager
storage_manager.save_data('AAPL', 150.0)
storage_manager.close()
