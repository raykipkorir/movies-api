import motor.motor_asyncio
from app.config import settings

# database integration - mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
db = client[settings.MONGO_INITDB_DATABASE]
