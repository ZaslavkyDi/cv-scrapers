from cv_common_library.message_brokers.kafka.base.producer import KafkaProducer
from cv_common_library.message_brokers.kafka.config import get_kafka_global_settings
from cv_common_library.message_brokers.schemas import BaseMetadataSchema

from cv_scrapers.common.enums import ScraperSourceName
from cv_scrapers.common.schemas.candidates_result import CandidatesPageResultSchema
from cv_scrapers.producers.schemas import (
    CandidateResultOutgoingBodyMessageSchema,
    CandidateResultOutgoingMessageSchema,
)


class CandidatesResultKafkaProducer(KafkaProducer):
    _TOPIC = "cv-scrapers.candidates.request.result"
    _CLIENT_ID = "cv-scrappers.candidates_result_producer"

    def __init__(self) -> None:
        super().__init__(
            topic=self._TOPIC,
            client_id=self._CLIENT_ID,
            bootstrap_servers=get_kafka_global_settings().bootstrap_servers,
        )

    def send_candidates_result(
        self,
        request_id: str,
        page_result: CandidatesPageResultSchema,
        scraping_source: ScraperSourceName,
    ) -> None:
        kafka_message = CandidateResultOutgoingMessageSchema(
            metadata=BaseMetadataSchema(request_id=request_id),
            body=CandidateResultOutgoingBodyMessageSchema(
                page_result=page_result,
                scrapping_source=scraping_source,
            ),
        )
        super().send_kafka_message(value=kafka_message)
