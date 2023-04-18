# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted data -> Temporary containers (items) -> Storing in database

import scrapy


class ImdbScrapItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    year = scrapy.Field()
    casting = scrapy.Field()
    rating = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()