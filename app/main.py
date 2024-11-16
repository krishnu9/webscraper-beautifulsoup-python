from fastapi import BackgroundTasks, Depends, FastAPI

from app.auth import authenticate
from app.handlers.get_all_products import get_all_product_items
from app.tasks import scraping_task
from .database import DATABASE_URL, engine, metadata
from app.handlers.scrape import scrape_page, scrape_all_pages
from databases import Database
from .models import ScrapeRequest
from contextlib import asynccontextmanager

database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.connect()
        metadata.create_all(bind=engine)
        yield
    finally:
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    n, proxy = request.pages, request.proxy
    background_tasks.add_task(scraping_task, database, n)
    return {"message": f"Scraping {n} pages"}

@app.get("/products")
async def get_products():
    products = await get_all_product_items(database)
    return products

