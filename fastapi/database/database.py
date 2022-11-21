from os import environ
from motor.motor_asyncio import AsyncIOMotorClient


DATABASE_URL = f"mongodb://{environ['MONGO_INITDB_ROOT_USERNAME']}:{environ['MONGO_INITDB_ROOT_PASSWORD']}@mongodb/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(DATABASE_URL)
db = client.kijiji

real_estate_collection = db.get_collection("real_estates")

