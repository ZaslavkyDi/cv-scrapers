from typing import Any

import pytest

from app.scrapers.robotaua import RobotaUACandidatesJsonParser


@pytest.fixture(scope="class")
def json_candidates_page_1() -> str:
    with open("../tests/resources/robotaua/candidates_page_1.json") as file:
        yield file.read()


@pytest.fixture(scope="class")
def robota_ua_candidates_parser() -> RobotaUACandidatesJsonParser:
    return RobotaUACandidatesJsonParser()


class TestRobotaUACandidatesJsonParser:
    def test_parse_candidates(
        self,
        robota_ua_candidates_parser: RobotaUACandidatesJsonParser,
        json_candidates_page_1: str,
    ) -> None:
        contains_expected_candidates: list[dict[str, Any]] = [
            {
                "cv_url": "https://robota.ua/ua/cv/20383779",
                "position": "Офіс-менеджер",
                "name": "Дмитро",
                "compensation": "14\xa0000 грн.",
                "age": 26,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://robota.ua/ua/cv/14708401",
                "position": "Адміністратор",
                "name": "Любов Григорівна",
                "compensation": "20\xa0000 грн.",
                "age": 35,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://robota.ua/ua/cv/22769674",
                "position": "Адміністратор, бухгалтер",
                "name": "Ангеліна",
                "compensation": None,
                "age": 26,
                "location": "Чернівці",
            },
        ]

        result = robota_ua_candidates_parser.parse(
            json_content=json_candidates_page_1, page_number=1
        )

        assert result.page_number == 1
        assert len(result.candidates) == 16

        actual_candidates: list[dict[str, Any]] = result.model_dump()["candidates"]
        for exp_candidate in contains_expected_candidates:
            assert exp_candidate in actual_candidates

    def test_parse_total_resumes_number(
        self,
        robota_ua_candidates_parser: RobotaUACandidatesJsonParser,
        json_candidates_page_1: str,
    ) -> None:
        actual_total_resumes_number = robota_ua_candidates_parser.parse_total_resumes_number(
            json_content=json_candidates_page_1
        )

        assert actual_total_resumes_number == 16
