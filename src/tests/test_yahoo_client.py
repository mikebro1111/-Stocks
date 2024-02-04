import unittest
import requests_mock
from src.core.yahoo_client import YahooClient


class TestYahooClient(unittest.TestCase):
    @requests_mock.Mocker()
    def test_get_financial_data_success(self, m):
        symbol = "AAPL"
        mock_url = f"https://finance.yahoo.com/quote/{symbol}"
        m.get(mock_url, text='<td data-test="OPEN-value">150</td>')
        price = YahooClient.get_financial_data(symbol, mock_url)
        self.assertEqual(price, "150")

    @requests_mock.Mocker()
    def test_get_financial_data_failure(self, m):
        symbol = "AAPL"
        mock_url = f"https://finance.yahoo.com/quote/{symbol}"
        m.get(mock_url, status_code=404)
        price = YahooClient.get_financial_data(symbol, mock_url)
        self.assertIsNone(price)


if __name__ == '__main__':
    unittest.main()
