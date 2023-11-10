from pydantic import BaseModel, Field, UUID4

from app.common.enums import ScraperSourceName


class MetadataSchema(BaseModel):
    request_id: UUID4


class MessageSchema(BaseModel):
    metadata: MetadataSchema
    # body: BaseModel


class CandidateRequestMessageBodySchema(BaseModel):
    scraping_sources: list[ScraperSourceName] = Field(default=[ScraperSourceName.all])
    position: str = Field(default_factory=list)


class CandidateRequestIncomingMessageSchema(MessageSchema):
    body: CandidateRequestMessageBodySchema

