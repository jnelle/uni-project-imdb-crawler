from db.mongo import MongoService
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service = providers.Factory(
        MongoService,
        connection_url=config.connection_url,
    )
