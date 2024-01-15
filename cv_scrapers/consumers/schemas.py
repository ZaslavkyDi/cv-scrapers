from pydantic import UUID4, BaseModel, Field

from cv_scrapers.common.enums import ScraperSourceName


class MetadataSchema(BaseModel):
    request_id: UUID4 | None = None


class MessageSchema(BaseModel):
    metadata: MetadataSchema
    # body: BaseModel


class CandidateRequestMessageBodySchema(BaseModel):
    scraping_sources: list[ScraperSourceName] = Field(default=[ScraperSourceName.all])
    position: str = Field(default_factory=list)


class CandidateRequestIncomingMessageSchema(MessageSchema):
    body: CandidateRequestMessageBodySchema
