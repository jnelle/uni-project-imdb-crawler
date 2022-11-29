from dependency_injector import containers, providers

from db.mongo import MongoService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service = providers.Factory(
        MongoService,
        connection_url=config.connection_url,
    )
