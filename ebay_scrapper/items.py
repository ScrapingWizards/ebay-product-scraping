# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayItem(scrapy.Item):
    item_url = scrapy.Field()
    item_title = scrapy.Field()
    item_condition = scrapy.Field()
    item_price = scrapy.Field()
    images = scrapy.Field()
    seller = scrapy.Field()
    seller_url = scrapy.Field()
    item_specification = scrapy.Field()
    category = scrapy.Field()
    category_id = scrapy.Field()
    category_tree_names = scrapy.Field()
    category_tree_ids = scrapy.Field()
    item_sold = scrapy.Field()
    item_reviews_percentage = scrapy.Field()
    item_rating_details = scrapy.Field()
    item_seller_feedback = scrapy.Field()
    status = scrapy.Field()
    error_info = scrapy.Field()
