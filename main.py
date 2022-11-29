import asyncio
from dotenv import load_dotenv

from provider.db_provider import Container
from imdb.reviews import get_reviews


load_dotenv()


async def main(container: Container):
    await get_reviews()

if __name__ == "__main__":
    container = Container()

    container.config.connection_url.from_env(
        "MONGO_CONNECTION_URL", required=True)
    container.wire(modules=[__name__])
    asyncio.run(main(container))
