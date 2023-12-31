import logging
import traceback

import scrapy
from ordered_set import OrderedSet

from ebay_scrapper.clean_utils import clean_price
from ebay_scrapper.items import EbayItem


class ItemDetailsSpider(scrapy.Spider):
    name = 'details_spider'

    def start_requests(self):
        # if listing is ready we can fetch data from mongo server
        # client, db = MongoDBPipeline.custom_client_from_crawler(self.crawler)
        # listing_data  = db['listing_data_collection'].find({})
        # urls = [url.get('url') for url in listing_data]
        # client.close()

        urls = [
            "https://www.ebay.de/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=kfz_elektrik&store_name=woospakfzteile&LH_ItemCondition=3&_ipg=240&_oac=1&store_cat=0"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.filter_page_parser)

    def filter_page_parser(self, response):
        logging.info('[x] Start Scrapping Filter Page')
        products_details_url = response.css('.srp-results .s-item__pl-on-bottom .s-item__info a::attr(href)').getall()
        for index, url in enumerate(products_details_url, 1):
            yield scrapy.Request(url=url, callback=self.details_page_parse)
            if index == 1:
                break

    def details_page_parse(self, response):
        logging.info(f'[x] Details Page {response.url}')
        product_details = EbayItem()
        product_details['status'] = 1
        product_details['item_url'] = response.url
        try:
            # main info
            base_info_obj = self._scrap_base_info(response)
            product_details.update(**base_info_obj)

            # category info extracted
            category_obj = self._scrap_category(response)
            product_details.update(**category_obj)

            # gallery
            galley_obj = self._scrap_gallery(response)
            product_details.update(**galley_obj)

            # seller info
            seller_info = self._scrap_seller_info(response)
            product_details.update(**seller_info)

            # about this item container
            item_specification = self._scrap_item_specification(response)
            product_details.update(**item_specification)

            # navigation section
            item_specification = self._scrap_item_specification(response)
            product_details.update(**item_specification)
        except Exception as e:
            exception_info = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
            product_details['status'] = 0
            product_details['error_info'] = exception_info
        finally:
            yield product_details

    def _scrap_base_info(self, response):
        data_obj = {}
        # main info
        title_text = "".join(response.css('.x-item-title__mainTitle ::text').getall()).strip()
        item_condition_element = response.css('.x-item-condition-value ::text').get().strip()
        primary_price = response.css('.x-price-primary ::text').get().strip()
        primary_price = clean_price(primary_price)
        data_obj['item_title'] = title_text
        data_obj['item_condition'] = item_condition_element
        data_obj['item_price'] = primary_price
        return data_obj

    def _scrap_gallery(self, response):
        data_obj = {}
        image_list = []
        image_gallery = response.css('.ux-image-filmstrip-carousel')
        if len(image_gallery) != 0:
            image_items = image_gallery.css('.ux-image-filmstrip-carousel-item')
            for item in image_items:
                # skip video thumbnails
                if not item.css('img::attr(alt)').get().startswith('Video') and len(image_list) < 4:
                    image_list.append(item.css('img::attr(src)').get().replace('s-l64', 's-l400'))
        else:
            img = response.css('.ux-image-carousel-item.active img::attr(src)').get()
            image_list.append(img)

        data_obj['images'] = image_list
        return data_obj

    def _scrap_seller_info(self, response):
        data_obj = {}

        seller_element = response.css('.ux-seller-section__item--seller')
        seller_name = seller_element.css('::text').get()
        seller_url = seller_element.css('a::attr(href)').get()
        data_obj['seller'] = seller_name
        data_obj['seller_url'] = seller_url
        return data_obj

    def _scrap_item_specification(self, response):
        data_obj = {}

        item_specification_elements = response.css('.x-about-this-item .ux-layout-section-evo__col')
        item_specification = {}

        for item in item_specification_elements:
            label = item.css('.ux-labels-values__labels ::text').get()
            value = item.css('.ux-labels-values__values ::text').get()
            if label is not None:
                item_specification[label] = value
        data_obj['item_specification'] = item_specification
        return data_obj

    def _scrap_category(self, response):
        data_obj = {}
        category_tree_elements = response.css('.breadcrumbs li a')
        category_tree_names = OrderedSet()
        category_tree_ids = OrderedSet()
        parent_category_index = -1
        for item in category_tree_elements:
            url = item.css("::attr(href)").get()
            if not url.startswith('#'):
                url_components = item.css("::attr(href)").get().split('/')
                if url_components[-2].lower() != 'p':
                    id = url_components[-2]
                else:
                    id = url_components[-1]
                    parent_category_index = -2
                name = item.css("::text").get()
                category_tree_ids.append(id)
                category_tree_names.append(name)

        category_name = category_tree_names[parent_category_index]
        category_id = category_tree_ids[-1]
        data_obj['category'] = category_name
        data_obj['category_id'] = category_id
        data_obj['category_tree_names'] = list(category_tree_names)
        data_obj['category_tree_ids'] = list(category_tree_ids)
        return data_obj
