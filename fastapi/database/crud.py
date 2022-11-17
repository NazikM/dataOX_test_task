import pymongo
from datetime import datetime
from database.database import real_estate_collection


async def list_by_price():
    data = real_estate_collection.find({
        'price': {'$ne': "Please Contact"}
        }, {'_id': 0}).sort("price", pymongo.ASCENDING)
    return await data.to_list(None)

async def list_by_price2(min_price, max_price):
    filtering = {'$ne': "Please Contact"}
    if max_price:
        filtering['$lt'] = max_price
    if min_price:
        filtering['$gt'] = min_price
    data = real_estate_collection.find({
        'price': filtering
        }, {'_id': 0}).sort("price", pymongo.ASCENDING)
    
    return await data

async def list_by_date2(min_date, max_date):
    filtering = {}
    if max_date:
        max_date = datetime.strptime(max_date, '%Y-%m-%dT%H:%M:%S')
        filtering['$lt'] = max_date
    if min_date:
        min_date = datetime.strptime(min_date, '%Y-%m-%dT%H:%M:%S')
        filtering['$gt'] = min_date
    data = real_estate_collection.find({
        'posted': filtering
        }, {'_id': 0}).sort("price", pymongo.ASCENDING)
    
    return await data


async def list_by_data():
    data = real_estate_collection.find(projection={'_id': 0}).sort("posted", pymongo.ASCENDING)
    return await data.to_list(None)

async def get_by_embeded_item(query_dict):
    return await real_estate_collection.find(query_dict, {'_id': 0}).to_list(None)
