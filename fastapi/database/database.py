from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_URL = "mongodb://admin:admin@mongodb/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(DATABASE_URL)
db = client.kijiji

real_estate_collection = db.get_collection("real_estates")

