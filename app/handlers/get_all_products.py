
from databases import Database
from app.database_utils import ProductDAO


async def get_all_product_items(db: Database):
    product_dao = ProductDAO(db)
    products = await product_dao.get_all()
    return products
