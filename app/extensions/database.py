import motor.motor_asyncio as motor
from app.config import settings

# database integration - mongodb
client = motor.AsyncIOMotorClient(settings.DATABASE_URL)
db = client[settings.MONGO_INITDB_DATABASE]
