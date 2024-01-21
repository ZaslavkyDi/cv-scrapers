import asyncio

from cv_scrapers.common.logger import init_logging
from cv_scrapers.consumers.candidates_request_consumer_kafka import CandidatesRequestConsumerKafka
from cv_scrapers.registries import consumers


async def main() -> None:
    init_logging()
    candidates_consumer: CandidatesRequestConsumerKafka = consumers.get("candidates_request_consumer_kafka")
    await candidates_consumer.start_consuming()


if __name__ == "__main__":
    asyncio.run(main())
