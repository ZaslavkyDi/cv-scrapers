import asyncio
import logging
from collections.abc import Awaitable
from typing import ClassVar, Self

from confluent_kafka import Message
from cv_common_library.message_brokers.kafka.base.consumer import BaseKafkaConsumer
from cv_common_library.message_brokers.kafka.config import get_kafka_global_settings

from cv_scrapers.common.enums import ScraperSourceName
from cv_scrapers.consumers.schemas import CandidateRequestIncomingMessageSchema
from cv_scrapers.producers.candidate_result_producer import CandidatesResultKafkaProducer
from cv_scrapers.registries import consumers
from cv_scrapers.scrapers.base.executor import BaseAsyncExecutor
from cv_scrapers.scrapers.robotaua.executor import RobotaUAExecutor
from cv_scrapers.scrapers.workua.executor import WorkUAExecutor

logger = logging.getLogger(__name__)


@consumers.register("candidates_request_consumer_kafka")
class CandidatesRequestConsumerKafka(BaseKafkaConsumer[CandidateRequestIncomingMessageSchema]):
    """
    A Kafka consumer for candidate requests.

    This consumer listens to the "cv-scrapers.candidates.request" topic and initiates scraping tasks
    based on the incoming messages. The scraping tasks are handled by executors specified in the
    `_SCRAPER_EXECUTORS` dictionary.

    Examples:
        async def main() -> None:
            consumer = CandidatesRequestConsumerKafka()
            await consumer.start_consuming()
            await asyncio.Future()

        if __name__ == "__main__":
            asyncio.run(main())
    """

    _TOPICS: ClassVar[list[str]] = [
        "cv-scrapers.candidates.request",
    ]
    _GROUP_ID = "cv-scrapers.candidates.request"

    _SCRAPER_EXECUTORS: ClassVar[dict[ScraperSourceName, type[BaseAsyncExecutor]]] = {
        ScraperSourceName.robotaua: RobotaUAExecutor,
        ScraperSourceName.workua: WorkUAExecutor,
    }

    def __init__(self, candidate_result_producer: CandidatesResultKafkaProducer) -> None:
        super().__init__(
            group_id=self._GROUP_ID,
            topics_to_subscribe=self._TOPICS,
            bootstrap_servers=get_kafka_global_settings().bootstrap_servers,
        )
        self._candidate_result_producer = candidate_result_producer

    @classmethod
    def create_instance(cls) -> Self:
        """
        Factory method for Kafka consumer.

        Returns:
            CandidatesRequestConsumerKafka: A new CandidatesRequestConsumerKafka instance.
        """
        candidate_result_producer = CandidatesResultKafkaProducer()
        return cls(candidate_result_producer)

    async def process_message(self, message: Message) -> None:
        try:
            message_model = CandidateRequestIncomingMessageSchema.model_validate_json(
                message.value()
            )
            logger.info(f"Received message: {message_model.model_dump()}")
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
        pages = await executor.run(position=position)

        for page_result in pages:
            self._candidate_result_producer.send_candidates_result(
                request_id=request_id,
                page_result=page_result,
                scraping_source=scraping_source,
            )
