import unittest
import requests_mock
from unittest.mock import patch
from src.core.database.wiki_client import WikiClient


class TestWikiClient(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.mongo_storage = None

    @requests_mock.Mocker()
    def test_get_wiki_symbols(self, m):
        mock_url = "https://example.com/wiki"
        mock_response = "<html><body><table class='wikitable sortable'>...</table></body></html>"
        m.get(mock_url, text=mock_response)

        symbols = WikiClient.get_wiki_symbols(mock_url)
        self.assertIsNotNone(symbols)
        # Additional assertions based on expected symbols from mock_response

    # Continuing from your existing TestMongoStorage class...

    @patch('mongo_storage.MongoClient')
    def test_find(self, mock_client):
        # Mock the MongoClient and its return values for the find operation
        mock_collection = mock_client.return_value.__getitem__.return_value.__getitem__
        mock_collection.find.return_value = [{"symbol": "AAPL", "price": 150}]
        result = self.mongo_storage.find({"symbol": "AAPL"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['symbol'], "AAPL")

    @patch('mongo_storage.MongoClient')
    def test_update_one(self, mock_client):
        # Mock the MongoClient and its return values for the update_one operation
        mock_collection = mock_client.return_value.__getitem__.return_value.__getitem__
        mock_collection.update_one.return_value.matched_count = 1
        mock_collection.find.return_value = [{"symbol": "AAPL", "price": 155}]
        result = self.mongo_storage.update_one({"symbol": "AAPL"}, {"price": 155})
        self.assertIsNotNone(result)
        self.assertEqual(result['price'], 155)

    # Similar approach for testing update_many, delete_one, delete_many

    if __name__ == '__main__':
        unittest.main()


if __name__ == '__main__':
    unittest.main()
