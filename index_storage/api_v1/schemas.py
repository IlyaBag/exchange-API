from datetime import datetime

from pydantic import BaseModel


class IndexPriceSave(BaseModel):
    ticker: str
    price: float


class IndexPrice(BaseModel):
    ticker: str
    price: float
    unix_timestamp: datetime
