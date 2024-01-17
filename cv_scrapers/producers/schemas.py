from cv_common_library.message_brokers.schemas import BaseMessageSchema
from pydantic import BaseModel

from cv_scrapers.common.enums import ScraperSourceName
from cv_scrapers.common.schemas.candidates_result import CandidatesPageResultSchema


class CandidateResultOutgoingBodyMessageSchema(BaseModel):
    page_result: CandidatesPageResultSchema
    scrapping_source: ScraperSourceName


class CandidateResultOutgoingMessageSchema(BaseMessageSchema):
    """
    Message schema example:
    {
        "metadata": {
            "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        "body": {
            "page_result": {
                "candidates": [
                    {
                        "name": "John Doe",
                        "position": "Software Engineer",
                        "location": "San Francisco, CA",
                        "source": "LinkedIn",
                        "url": "https://www.linkedin.com/in/johndoe/"
                    },
                ],
                "page_number": 1,
            },
            "scrapping_source": "robotaua"
        }
    }
    """

    body: CandidateResultOutgoingBodyMessageSchema
