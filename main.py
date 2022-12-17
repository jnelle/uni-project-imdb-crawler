import asyncio
import logging

from dotenv import load_dotenv
from imdb.reviews import get_reviews, get_top_movies
from provider.db_provider import Container

load_dotenv()


async def main(container: Container):
    await get_top_movies()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    container = Container()
    container.config.connection_url.from_env(
        "MONGO_CONNECTION_URL", required=True)
    container.wire(modules=[__name__])

    asyncio.run(main(container))
