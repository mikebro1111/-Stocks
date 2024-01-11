from dataclasses import dataclass


@dataclass
class Prices:
    """
    Represents the pricing information of a stock.

    Attributes:
        symbol (str): The stock symbol.
        price (float): The price of the stock.
        date (str): The date when the price was recorded.
    """
    symbol: str
    price: float
    date: str
