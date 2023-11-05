from typing import Generic, TypeVar

from pydantic import BaseModel

from app.common.schemas.validators import NotEmptyNullableString

CANDIDATE_T = TypeVar("CANDIDATE_T", bound=BaseModel)


class CandidateDetailsSchema(BaseModel):
    cv_url: str
    position: str
    name: str
    compensation: NotEmptyNullableString = None
    age: int | None = None
    location: NotEmptyNullableString = None


class CandidatesPageResultSchema(BaseModel):
    candidates: list[CandidateDetailsSchema]
    page_number: int
