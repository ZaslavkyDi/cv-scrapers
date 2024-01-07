from functools import lru_cache

from cv_scrapers.message_broker.congif.settings import RabbitMQSettings


@lru_cache
def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()
