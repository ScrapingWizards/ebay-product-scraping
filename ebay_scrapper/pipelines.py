import sys

import pymongo


class MongoDBPipeline:

    def __init__(self, mongodb_uri, mongodb_db, collection):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        self.collection = collection
        if not self.mongodb_uri: sys.exit(
            "You need to provide a Connection String. and collection")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'EbayScraping'),
            collection=crawler.settings.get('MONGODB_COLLECTION', 'detail_data_collection'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        self.db[self.collection].insert_one(data)
        return item
