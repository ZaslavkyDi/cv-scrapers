from logging import getLogger


from app.common.schemas.candidates_result import CandidatesPageResultSchema, CandidateDetailsSchema
from app.scrapers.robotaua.config import get_robotaua_settings
from app.scrapers.robotaua.schemas.response import ResumeSearchResponsePayload

logger = getLogger(__name__)


class RobotaUACandidatesJsonParser:

    def parse(self, json_content: str, page_number: int | None = None) -> CandidatesPageResultSchema:
        page_result = ResumeSearchResponsePayload.model_validate_json(json_data=json_content)

        candidates: list[CandidateDetailsSchema] = []
        url_template = get_robotaua_settings().resume_url_template
        for doc in page_result.documents:
            candidates.append(
                CandidateDetailsSchema(
                    cv_url=url_template.format(resume_id=doc.resume_id),
                    position=doc.speciality,
                    name=doc.display_name,
                    compensation=doc.salary,
                    age=self._parse_age(raw_age=doc.age),
                    location=doc.city_name
                )
            )

        return CandidatesPageResultSchema(
            candidates=candidates,
            page_number=page_number,
        )

    @staticmethod
    def parse_total_resumes_number(json_content: str) -> int:
        page_result = ResumeSearchResponsePayload.model_validate_json(json_data=json_content)
        return page_result.total

    @staticmethod
    def parse_resume_request_step(json_content: str) -> int:
        page_result = ResumeSearchResponsePayload.model_validate_json(json_data=json_content)
        return page_result.requested_count

    @staticmethod
    def _parse_age(raw_age: str | None) -> int | None:
        if not raw_age:
            return None

        numbers = [int(i) for i in raw_age.split() if i.isdigit()]
        if not numbers:
            return None

        return numbers[0]
