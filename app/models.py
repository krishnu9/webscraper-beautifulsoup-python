from typing import Optional
from pydantic import BaseModel, PositiveInt


class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeRequest(BaseModel):
    pages: Optional[PositiveInt] = 1
    proxy: str