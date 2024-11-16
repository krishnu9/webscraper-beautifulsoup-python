from abc import ABC, abstractmethod

class Notification:
    def __init__(self, message: str, scrape_count: int, recipient: str):
        self.message = message
        self.scrape_count = scrape_count
        self.recipient = recipient

class NotificationService(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotificationService(NotificationService):
    def send(self, notification: Notification) -> None:
        print(f"Sending email to {notification.recipient}: {notification.message}")


class PrintNotificationService(NotificationService):
    def send(self, notification: Notification) -> None:
        print(f"---------- Scraping Notification ----------")
        print("Message:", notification.message)
        print("Scraped Count:", notification.scrape_count)