from os import environ
import pymongo


class KijijiPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(f"mongodb://{environ['MONGO_INITDB_ROOT_USERNAME']}:{environ['MONGO_INITDB_ROOT_PASSWORD']}@mongodb/?retryWrites=true&w=majority")
        self.db = self.client["kijiji"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['type'] == 'real_estate':
            if item.get('id'):
                return item
            self.db["real_estates"].insert_one(item['data'])
        else:
            self.db["authors"].insert_one(item['data'])
        return item
