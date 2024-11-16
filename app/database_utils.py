from .models import Product
from sqlalchemy import Column, Integer, String, Float, Table
from .database import metadata

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_title", String),
    Column("product_price", Float),
    Column("path_to_image", String)
)

# Strategy class to write Product objects to the database
class ProductDAO:
    def __init__(self, database):
        self.database = database

    async def create(self, product):
        query = products_table.insert().values(
            product_title=product.product_title,
            product_price=product.product_price,
            path_to_image=product.path_to_image
        )
        await self.database.execute(query)

    async def get_all(self):
        query = products_table.select()
        return await self.database.fetch_all(query)

    async def get_by_id(self, product_id):
        query = products_table.select().where(products_table.c.id == product_id)
        return await self.database.fetch_one(query)

    async def delete(self, product_id):
        query = products_table.delete().where(products_table.c.id == product_id)
        await self.database.execute(query)

    async def update(self, product_id, product):
        query = products_table.update().where(products_table.c.id == product_id).values(
            product_title=product.product_title,
            product_price=product.product_price,
            path_to_image=product.path_to_image
        )
        await self.database.execute(query)