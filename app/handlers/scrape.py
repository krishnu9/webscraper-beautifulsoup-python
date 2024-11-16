from databases import Database
import httpx
from bs4 import BeautifulSoup

from app.database_utils import ProductDAO
from app.image_utils import ImageFetcher
from app.notification import Notification
from ..models import Product
from pathlib import Path

script_dir = Path(__file__).resolve().parent

BASE_URL = "https://dentalstall.com/shop"

title_selector = '.woo-loop-product__title'
price_selector = '.amount'
image_src_selector = '.mf-product-thumbnail > a > img'

class Scraper:
    def __init__(self, db: Database):
        self.db = db

    async def fetch_html(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    
    async def parse_html(self, html: str) -> list[Product]:
        soup = BeautifulSoup(html, "html.parser")
        image_fetcher = ImageFetcher(script_dir, storage_strategy='fs')
        products = []
        for product_card in soup.select('.product-inner'):
            product_title = product_card.select_one(title_selector).text.strip()
            product_price = float(product_card.select_one(price_selector).text.strip()[1:])
            img_element = product_card.select_one(image_src_selector)

            # Storing images in a folder
            if img_element and 'src' in img_element.attrs:
                img_url = img_element['data-lazy-src']
                print(f"Image URL: {img_url}")
                file_path = await image_fetcher.fetch_image_and_save_to_fs(img_url)
                print(f"File Path: {file_path}")

            # Create a Product object
            product = Product(
                product_title=product_title,
                product_price=product_price,
                path_to_image=str(file_path)
            )
            
            products.append(product)
        
        return products

    async def write_products_to_db(self, products: list[Product]):
        product_dao = ProductDAO(self.db)
        for product in products:
            await product_dao.create(product)

async def scrape_page(db: Database, page: int):
    scraper = Scraper(db)
    page_url = f"{BASE_URL}/" if page == 1 else f"{BASE_URL}/page/{page}/"
    print(f"Scraping page: {page_url}")
    try:
        html = await scraper.fetch_html(page_url)
        products = await scraper.parse_html(html)
        await scraper.write_products_to_db(products)
        # print(f"Scraped {products}")
        return products
    except Exception as e:
        # return {"message": "Failed to scrape", "error": str(e)}
        raise e

# Route Handler   
async def scrape_all_pages(db: Database, n: int):
    response = []
    scraped_count = 0
    scrape_success = False
    for page in range(n):
        try:
            r = await scrape_page(db, page+1)
            response.extend(r)
            scraped_count += len(r)
        except Exception as e:
            print(f"Failed to scrape page {page+1}: {str(e)}")
    return Notification("Scraping complete", scraped_count, "console")