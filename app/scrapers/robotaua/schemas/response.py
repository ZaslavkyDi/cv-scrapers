from pydantic import BaseModel, ConfigDict, Field

from app.common.schemas.validators import NotEmptyNullableString


class CandidateData(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resume_id: int = Field(..., alias="resumeId")
    speciality: str
    display_name: str = Field(..., alias="displayName")
    age: NotEmptyNullableString = None
    salary: NotEmptyNullableString = None
    city_name: NotEmptyNullableString = Field(None, alias="cityName")


class ResumeSearchResponsePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    total: int
    total_full: int = Field(..., alias="totalFull")
    search_api_request_url: str = Field(..., alias="searchApiRequestUrl")
    documents: list[CandidateData]
    requested_count: int = Field(..., alias="requestedCount")
