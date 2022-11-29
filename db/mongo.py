import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from models.model import Review


class MongoService:
    def __init__(self, connection_url: str) -> None:
        self.client: AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(
            connection_url, serverSelectionTimeoutMS=5000).main
        self.collection = self.client.reviews

    async def add_review(self, review: Review):
        await self.collection.insert_one(review.dict())
