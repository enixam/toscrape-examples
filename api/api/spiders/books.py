import scrapy
import json
import time
from api.items import (BookItem, BookLoader)
from scrapy.exceptions import CloseSpider


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        "https://openlibrary.org/subjects/picture_books.json?limit=12"]

    increament_by = 12
    offset = 0

    def parse(self, response):

        if response.status == 500:
            raise CloseSpider("reach api end")

        resp = json.loads(response.body)
        for book in resp["works"]:
            loader = BookLoader(item=BookItem())
            loader.add_value("title", book["title"])
            loader.add_value("author", book["authors"])
            loader.add_value(
                "availability", {} if "availability" not in book else book["availability"])
            loader.add_value("checked_out", book["checked_out"])
            loader.add_value("edition_count", book["edition_count"])
            loader.add_value("first_publish_year", book["first_publish_year"])
            loader.add_value("has_fulltext", book["has_fulltext"])
            loader.add_value("subjects", book["subject"])
            yield loader.load_item()

        time.sleep(5)
        self.offset += self.increament_by
        next_url = f"https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}"
        yield scrapy.Request(next_url, callback=self.parse)
