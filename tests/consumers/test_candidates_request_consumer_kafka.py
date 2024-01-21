import json
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from confluent_kafka import Message

from cv_scrapers.common.enums import ScraperSourceName
from cv_scrapers.consumers.candidates_request_consumer import CandidatesRequestConsumerKafka


@pytest.fixture
def candidates_kafka_consumer() -> CandidatesRequestConsumerKafka:
    return CandidatesRequestConsumerKafka(
        candidate_result_producer=MagicMock(),
    )


def build_kafka_message_request_mock(scraping_sources: list[ScraperSourceName]) -> MagicMock:
    # Create a mock Kafka message
    message = MagicMock(spec=Message)
    message.value.return_value = json.dumps(
        {
            "metadata": {"request_id": "b2d8d0f7-7e0a-4b1f-8f9b-0b3d5f7e0a4b"},
            "body": {
                "scraping_sources": scraping_sources,
                "position": "Python developer",
            },
        }
    )
    return message


@patch("cv_scrapers.scrapers.robotaua.executor.RobotaUAExecutor.run")
@pytest.mark.asyncio
async def test_check_that_robotaua_executor_is_triggered(
    mock_robotaua_executor_run: Mock,
    candidates_kafka_consumer: CandidatesRequestConsumerKafka,
) -> None:
    kafka_message_request: MagicMock = build_kafka_message_request_mock(
        scraping_sources=[ScraperSourceName.robotaua]
    )
    mock_robotaua_executor_run.return_value = AsyncMock(return_value="Fake Result")

    await candidates_kafka_consumer.process_message(kafka_message_request)

    mock_robotaua_executor_run.assert_called_once_with(position="Python developer")


@patch("cv_scrapers.scrapers.workua.executor.WorkUAExecutor.run")
@pytest.mark.asyncio
async def test_check_that_workua_executor_is_triggered(
    mock_workua_executor_run: Mock,
    candidates_kafka_consumer: CandidatesRequestConsumerKafka,
) -> None:
    kafka_message_request: MagicMock = build_kafka_message_request_mock(
        scraping_sources=[ScraperSourceName.workua]
    )
    mock_workua_executor_run.return_value = AsyncMock(return_value="Fake Result")

    await candidates_kafka_consumer.process_message(kafka_message_request)

    mock_workua_executor_run.assert_called_once_with(position="Python developer")


@patch("cv_scrapers.scrapers.robotaua.executor.RobotaUAExecutor.run")
@patch("cv_scrapers.scrapers.workua.executor.WorkUAExecutor.run")
@pytest.mark.asyncio
async def test_all_executors_run(
    mock_workua_executor_run: Mock,
    mock_robotaua_executor_run: Mock,
    candidates_kafka_consumer: CandidatesRequestConsumerKafka,
) -> None:
    request_position = "Python developer"

    kafka_message_request: MagicMock = build_kafka_message_request_mock(
        scraping_sources=[ScraperSourceName.all]
    )
    mock_workua_executor_run.return_value = AsyncMock(return_value="Fake Result WorkUA")
    mock_robotaua_executor_run.return_value = AsyncMock(return_value="Fake Result RobotaUA")

    await candidates_kafka_consumer.process_message(kafka_message_request)

    mock_workua_executor_run.assert_called_once_with(position=request_position)
    mock_robotaua_executor_run.assert_called_once_with(position=request_position)
