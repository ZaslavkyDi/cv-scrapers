from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from cv_scrapers.scrapers.robotaua.config.enums import SearchPeriod


class ResumeSearchRequestPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int
    key_words: str = Field(..., alias="keyWords")
    period: str = SearchPeriod.TODAY.value
    sort: Literal["UpdateDate"] = "UpdateDate"
    search_type: Literal["default"] = Field("default", alias="searchType")
    ukrainian: bool = True
    only_disliked: bool = Field(False, alias="onlyDisliked")
    only_favorite: bool = Field(False, alias="onlyFavorite")
    only_with_current_notebook_notes: bool = Field(False, alias="onlyWithCurrentNotebookNotes")
    show_cv_without_salary: bool = Field(True, alias="showCvWithoutSalary")
    sex: Literal["Any"] = "Any"
    city_id: int = Field(alias="cityId")
    inside: bool = False
    only_new: bool = Field(False, alias="onlyNew")
    moveability: bool = True
    only_moveability: bool = Field(False, alias="onlyMoveability")
    has_photo: bool = Field(False, alias="hasPhoto")
    only_viewed: bool = Field(False, alias="onlyViewed")
    only_with_opened_contacts: bool = Field(False, alias="onlyWithOpenedContacts")
    only_students: bool = Field(False, alias="onlyStudents")
    search_context: Literal["Main"] = "Main"
