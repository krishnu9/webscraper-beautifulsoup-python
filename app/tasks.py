from databases import Database
from fastapi import BackgroundTasks
import requests
from app.handlers.scrape import scrape_all_pages
from app.notification import Notification, PrintNotificationService, EmailNotificationService
from tenacity import before_log, retry, stop_after_attempt, wait_fixed

from app.retry import print_retry_attempt
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.WARN)

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), before=before_log(logger, logging.DEBUG), reraise=True)
async def scraping_task(db: Database, n: int):
    if db.is_connected and n > 0:
        print("Scraping task started")

    notification = PrintNotificationService()

    try:
        scraping_details = await scrape_all_pages(db, n)
        # Send notification if scraping is successful
        notification.send(scraping_details)

    except Exception as e:
        print(f"Failed to scrape: {str(e)}")
        # Send notification if scraping fails 
        notification.send(Notification(str(e), 0, "console"))

