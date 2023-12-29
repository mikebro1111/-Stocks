from dataclasses import dataclass


@dataclass
class Prices:
    symbol: str
    price: float
    date: str
