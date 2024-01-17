from cv_common_library.message_brokers.schemas import BaseMessageSchema
from pydantic import BaseModel, Field

from cv_scrapers.common.enums import ScraperSourceName


class CandidateRequestMessageBodySchema(BaseModel):
    scraping_sources: list[ScraperSourceName] = Field(default=[ScraperSourceName.all])
    position: str = Field(default_factory=list)


class CandidateRequestIncomingMessageSchema(BaseMessageSchema):
    """
    Message schema example:
    {
        "metadata": {
            "request_id": "b2d8d0f7-7e0a-4b1f-8f9b-0b3d5f7e0a4b"
        },
        "body": {
            "scraping_sources": [
                "robotaua",
                "workua"
            ],
            "position": "Python developer"
        }
    }
    """

    body: CandidateRequestMessageBodySchema
