import unittest
from src.core.database.mongo_storage import MongoStorage
from unittest.mock import MagicMock, patch


class TestMongoStorage(unittest.TestCase):
    @patch('pymongo.MongoClient')
    def test_save_one(self, mock_client):
        mock_collection = mock_client.return_value.__getitem__.return_value.__getitem__
        mongo_storage = MongoStorage("mock_db_url")
        test_data = {"symbol": "AAPL", "price": 150}
        mongo_storage.save_one(test_data)
        mock_collection.assert_called_once_with(test_data)


if __name__ == '__main__':
    unittest.main()
