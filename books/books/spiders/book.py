import scrapy
import re

class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        links = response.css(".product_pod a").xpath(".//@href").getall()
        book_links = map(lambda l: "https://books.toscrape.com/catalogue/" + l, links)
        page = re.search(r".+page\-(\d{1,2}).+", response.url).group(1)
        yield from response.follow_all(book_links, callback = self.parse_book, cb_kwargs = {"page": page})

        next_link = response.css(".pager .next a")
        if next_link is not None:
            href =  next_link.xpath(".//@href").get()
            link = "https://books.toscrape.com/catalogue/" + href
            yield scrapy.Request(link, callback = self.parse)


    def parse_book(self, response, page):
        def extract(css = "", xpath = ""):
            if css:
                return response.css(css).get(default="").strip()
            if xpath:
                return response.xpath(xpath).get(default="").strip()

        def rating2num(rating):
            switcher = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5,
                "": None,
            }

            return switcher.get(rating, None)
        yield {
            "title": extract(".product_main h1::text"),
            "img": extract(xpath = ".//img/@src"),
            "rating": rating2num(extract(xpath = ".//p[contains(@class, 'star-rating')]/@class")[12:]),
            "description": extract("#product_description + p::text"),
            "page": page
        }

