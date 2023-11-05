from pydantic import BaseModel, validator, field_validator

from app.workua.schemas.validators import NotEmptyNullableString


class WorkUACandidateSchema(BaseModel):
    cv_url: str
    position: str
    name: str
    compensation: NotEmptyNullableString = None
    age: int | None = None
    location: NotEmptyNullableString = None

    @field_validator("name", mode="before")
    @classmethod
    def set_up_place_holder(cls, name: str) -> str:
        if name == "Приховано":
            name = "Hidden"
        return name


class CandidatesPageResultSchema(BaseModel):
    candidates: list[WorkUACandidateSchema]
    page_number: int
