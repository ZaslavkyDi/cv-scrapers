import asyncio
import logging
from collections.abc import Awaitable

from confluent_kafka import Message
from cv_common_library.message_brokers.kafka.base import kafka_consumer_settings
from cv_common_library.message_brokers.kafka.base.consumer import BaseKafkaConsumer

from cv_scrapers.common.enums import ScraperSourceName
from cv_scrapers.common.logger import init_logging
from cv_scrapers.consumers.schemas import CandidateRequestIncomingMessageSchema
from cv_scrapers.message_broker.base.connection import get_rabbitmq_connection
from cv_scrapers.scrapers.base.executor import BaseAsyncExecutor
from cv_scrapers.scrapers.robotaua.executor import RobotaUAExecutor
from cv_scrapers.scrapers.workua.executor import WorkUAExecutor

logger = logging.getLogger(__name__)


class CandidatesRequestConsumerKafka(BaseKafkaConsumer[CandidateRequestIncomingMessageSchema]):
    _TOPICS: list[str] = ["cv-scrapers.candidates.request",]
    _GROUP_ID = "cv-scrapers.candidates.request"

    _SCRAPER_EXECUTORS: dict[ScraperSourceName, type[BaseAsyncExecutor]] = {
        ScraperSourceName.robotaua: RobotaUAExecutor,
        ScraperSourceName.workua: WorkUAExecutor,
    }

    def __init__(self) -> None:
        super().__init__(
            group_id=self._GROUP_ID,
            topics_to_subscribe=self._TOPICS,
            bootstrap_servers="localhost:9092",
        )

    async def process_message(self, message: Message) -> None:
        try:
            payload = message.value()
            message_model = CandidateRequestIncomingMessageSchema.model_validate_json(payload)
            await self._initiate_scraping(message_model)
        except Exception as e:
            logger.exception(f"Error in {self.topics}: {e!s}")

    async def _initiate_scraping(
        self, message_model: CandidateRequestIncomingMessageSchema
    ) -> None:
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
    consumer = CandidatesRequestConsumerKafka()

    await consumer.start_consuming()
    await asyncio.Future()


if __name__ == "__main__":
    init_logging()
    asyncio.run(main())
