# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, Compose, TakeFirst
from api.utils.processors import SelectAuthor, SelectFields, TakeTheFirst


class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    availability = scrapy.Field()
    checked_out = scrapy.Field()
    edition_count = scrapy.Field()
    first_publish_year = scrapy.Field()
    has_fulltext = scrapy.Field()
    subjects = scrapy.Field()


class BookLoader(ItemLoader):
    title_in = MapCompose(str.title)
    title_out = TakeFirst()
    author_in = SelectAuthor
    availability_in = Compose(lambda l: l[0], SelectFields(
        ["status", "available_to_waitlist", "availability_to_borrow"]))
    subject_in = TakeTheFirst(5)
