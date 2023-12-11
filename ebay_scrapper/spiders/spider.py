import logging

import scrapy


class ItemDetailsSpider(scrapy.Spider):
    name = 'spider'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': logging.ERROR
    }
    start_urls = [
        "https://www.ebay.de/itm/364088301643?hash=item54c55a984b%3Ag%3AW%7EoAAOSw2BBlDVai&LH_ItemCondition=3"
    ]

    def parse(self, response):
        # base info
        title_text = "".join(response.css('.x-item-title__mainTitle ::text').getall()).strip()
        item_condition_element = response.css('.x-item-condition-value ::text').get().strip()
        primary_price = response.css('.x-price-primary ::text').get().strip()
        print(title_text, item_condition_element, primary_price)

        # gallery
        # TODO : when there is one image
        image_list = []
        image_gallery = response.css('.ux-image-filmstrip-carousel')
        if len(image_list) != 0:
            image_items = image_gallery.css('.ux-image-filmstrip-carousel-item')
            for item in image_items:
                # skip video thumbnails
                if not item.css('img::attr(alt)').get().startswith('Video') and len(image_list) < 4:
                    image_list.append(item.css('img::attr(src)').get().replace('s-l64', 's-l400'))
        else:
            img = response.css('.ux-image-carousel-item.active img::attr(src)').get()
            image_list.append(img)
        # print(image_list)
        # seller info
        seller_element = response.css('.ux-seller-section__item--seller')
        seller_name = seller_element.css('::text').get()
        seller_url = seller_element.css('a::attr(href)').get()
        # print(seller_url, seller_name)

        # about this item container
        item_specification_elements = response.css('.x-about-this-item .ux-layout-section-evo__col')
        for item in item_specification_elements:
            label = item.css('.ux-labels-values__labels ::text').get()
            value = item.css('.ux-labels-values__values ::text').get()
            # print(label, "====", value)

        # navigation section
        # TODO try catch when index -2 is not exist
        category_tree_elements = response.css('.breadcrumbs li')
        category_element = category_tree_elements[-2]

        category_tree = category_tree_elements.css("::text").getall()
        category_name = category_element.css('::text').get()
        category_id = category_element.css('::attr(href)').get().split('/')[-2]
        # print(category_name, category_id)

        # review
        general_review_element = response.css('.d-stores-info-categories__container__info__section__item')
        reviews_percentage = "".join(general_review_element[0].css('::text').getall())
        sold_item = ''.join(general_review_element[1].css('::text').getall())

        # detailed rating
        detailed_seller_rating_element = response.css('.fdbk-detail-seller-rating')
        detailed_seller_rating = {}
        for item in detailed_seller_rating_element:
            label = item.css('.fdbk-detail-seller-rating__label ::text').get()
            value = item.css('.fdbk-detail-seller-rating__value ::text').get()
            detailed_seller_rating[label] = value
        # print(detailed_seller_rating)
        # detailed rating
        fdbk_data = []
        seller_rating_cards = response.css('.fdbk-container')
        for item in seller_rating_cards:
            fdbk_username = item.css('.fdbk-container__details__info__username ::text').get()
            fdbk_detailed_comment = item.css('.fdbk-container__details__comment ::text').get()
            fdbk_item = item.css('.fdbk-container__details__item-link > a::attr(href)').get()
            fdbk_data.append({
                "fdbk_username": fdbk_username,
                "fdbk_detailed_comment": fdbk_detailed_comment,
                "fdbk_item": fdbk_item
            })
