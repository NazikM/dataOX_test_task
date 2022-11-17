# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo


class KijijiPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.gdlnwci.mongodb.net/?retryWrites=true&w=majority")
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
