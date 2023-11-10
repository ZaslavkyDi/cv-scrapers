import asyncio
import logging
import time
from typing import Type, Awaitable

from aio_pika.abc import AbstractIncomingMessage

from app.common.enums import ScraperSourceName
from app.common.logger import init_logging
from app.consumers.schemas import CandidateRequestIncomingMessageSchema
from app.message_broker.base import consumer
from app.message_broker.base.connection import get_rabbitmq_connection
from app.scrapers.base.executor import BaseAsyncExecutor
from app.scrapers.robotaua.executor import RobotaUAExecutor
from app.scrapers.workua.executor import WorkUAExecutor

logger = logging.getLogger(__name__)


class CandidatesRequestConsumer:

    _QUEUE_NAME = "cv-scrapers.candidates.request"
    _ROUTING_KEYS: tuple[str, ...] = ("candidates.request.scrape.v1",)
    _SCRAPER_EXECUTORS: dict[ScraperSourceName, Type[BaseAsyncExecutor]] = {
        ScraperSourceName.robotaua: RobotaUAExecutor,
        ScraperSourceName.workua: WorkUAExecutor,
    }

    def __init__(self, enable_x_dead_letter: bool = True) -> None:
        self._enable_x_dead_letter = enable_x_dead_letter

    async def consume_events(self) -> None:
        """This method is entrypoint for consuming RMQ messages (consumers)."""
        await consumer.consume_events(
            queue_name=self._QUEUE_NAME,
            routing_keys=self._ROUTING_KEYS,
            callback=self._process_event,
            enable_x_dead_letter=self._enable_x_dead_letter,
        )

    async def _process_event(self, message: AbstractIncomingMessage) -> None:
        async with message.process(ignore_processed=True):
            try:
                message_model = CandidateRequestIncomingMessageSchema.model_validate_json(message.body)
                await self._initiate_scraping(message_model)
            except Exception as e:
                logger.exception(f"Error in {self._QUEUE_NAME}: {str(e)}")
                await message.nack(requeue=False)
            else:
                await message.ack()

    async def _initiate_scraping(self, message_model: CandidateRequestIncomingMessageSchema) -> None:
        start_t = time.time()
        coros: list[Awaitable[None]] = []

        sources = message_model.body.scraping_sources
        if ScraperSourceName.all in sources:
            for src_name in self._SCRAPER_EXECUTORS.keys():
                coros.append(
                    self._create_task(
                        scraping_source=src_name,
                        position=message_model.body.position,
                        request_id=message_model.metadata.request_id,
                    )
                )
        else:
            for src_name in sources:
                coros.append(
                    self._create_task(
                        scraping_source=src_name,
                        position=message_model.body.position,
                        request_id=message_model.metadata.request_id,
                    )
                )

        await asyncio.gather(*coros)
        end_t = time.time()
        logger.info(
            f"Stop processing: {message_model.metadata.request_id} with sources: {sources}. "
            f"Taking time: {end_t - start_t}."
        )

    async def _create_task(
        self,
        scraping_source: ScraperSourceName,
        position: str,
        request_id: str,
    ) -> None:
        executor_class = self._SCRAPER_EXECUTORS.get(scraping_source)
        if not executor_class:
            logger.warning(f"Try to call unregistered scraping executor: {scraping_source}")
            return

        executor = executor_class()
        result = await executor.run(position=position)
        print(f"Request_id: {request_id}. Source: {scraping_source}.")
        # TODO: send to another queue


async def main() -> None:
    consumer = CandidatesRequestConsumer()

    try:
        await consumer.consume_events()
        await asyncio.Future()
    finally:
        connection = await get_rabbitmq_connection()
        await connection.close()

if __name__ == '__main__':
    init_logging()
    asyncio.run(main())