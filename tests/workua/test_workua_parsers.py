from pathlib import Path
from typing import Any

import pytest

from cv_scrapers.scrapers.workua.parsers import WorkUACandidatesHtmlParser


@pytest.fixture(scope="class")
def html_candidates_page_1() -> str:
    path = Path(__file__).parent.parent / "resources/workua/candidates_page_1.html"
    with open(path) as file:
        yield file.read()


@pytest.fixture(scope="class")
def html_candidates_page_2() -> str:
    path = Path(__file__).parent.parent / "resources/workua/candidates_page_2.html"
    with open(path) as file:
        yield file.read()


@pytest.fixture(scope="class")
def work_ua_candidates_parser() -> WorkUACandidatesHtmlParser:
    return WorkUACandidatesHtmlParser()


class TestWorkUACandidatesHtmlParser:
    def test_parse_candidates_page_1(
        self,
        work_ua_candidates_parser: WorkUACandidatesHtmlParser,
        html_candidates_page_1: str,
    ) -> None:
        contains_expected_candidates: list[dict[str, Any]] = [
            {
                "cv_url": "https://www.work.ua/resumes/8052197/",
                "position": "Менеджер\n\t\t\t\t\t\t\t\t\t\t\tз продажу, помічник\n\t\t\t\t\t\t\t\t\t\t\tкерівника",
                "name": "Олеся",
                "compensation": None,
                "age": 28,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://www.work.ua/resumes/10159664/",
                "position": "Консультант з\n\t\t\t\t\t\t\t\t\t\t\tпродажу",
                "name": "Дмитро",
                "compensation": None,
                "age": 18,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://www.work.ua/resumes/9199274/",
                "position": "Менеджер з\n\t\t\t\t\t\t\t\t\t\t\tпродажу",
                "name": "Віктор",
                "compensation": "15000 грн",
                "age": 20,
                "location": "Чернівці, Інші країни, Дистанційно",
            },
            {
                "cv_url": "https://www.work.ua/resumes/8677876/",
                "position": "Менеджер по\n\t\t\t\t\t\t\t\t\t\t\tпродажам",
                "name": "Ірина",
                "compensation": None,
                "age": 35,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://www.work.ua/resumes/7638972/",
                "position": "Менеджер по\n\t\t\t\t\t\t\t\t\t\t\tобработке\n\t\t\t\t\t\t\t\t\t\t\tзаказов",
                "name": "Аліна",
                "compensation": "13000 грн",
                "age": 18,
                "location": "Чернівці",
            },
        ]

        result = work_ua_candidates_parser.parse(html_content=html_candidates_page_1, url=None)

        assert result.page_number == 1
        assert len(result.candidates) == 14

        actual_candidates: list[dict[str, Any]] = result.model_dump()["candidates"]
        for exp_candidate in contains_expected_candidates:
            assert exp_candidate in actual_candidates

    def test_parse_last_page_number(
        self,
        work_ua_candidates_parser: WorkUACandidatesHtmlParser,
        html_candidates_page_1: str,
    ) -> None:
        expected_last_number = 23
        result = work_ua_candidates_parser.parse_last_page_number(
            content=html_candidates_page_1,
            url=None,
        )

        assert result == expected_last_number

    def test_parse_candidates_page_2(
        self,
        work_ua_candidates_parser: WorkUACandidatesHtmlParser,
        html_candidates_page_2: str,
    ) -> None:
        contains_expected_candidates: list[dict[str, Any]] = [
            {
                "cv_url": "https://www.work.ua/resumes/8052197/",
                "position": "Менеджер\n\t\t\t\t\t\t\t\t\t\t\tз продажу, помічник\n\t\t\t\t\t\t\t\t\t\t\tкерівника",
                "name": "Олеся",
                "compensation": None,
                "age": 28,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://www.work.ua/resumes/10159664/",
                "position": "Консультант з\n\t\t\t\t\t\t\t\t\t\t\tпродажу",
                "name": "Дмитро",
                "compensation": None,
                "age": 18,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://www.work.ua/resumes/9199274/",
                "position": "Менеджер з\n\t\t\t\t\t\t\t\t\t\t\tпродажу",
                "name": "Віктор",
                "compensation": "15000 грн",
                "age": 20,
                "location": "Чернівці, Інші країни, Дистанційно",
            },
            {
                "cv_url": "https://www.work.ua/resumes/8677876/",
                "position": "Менеджер по\n\t\t\t\t\t\t\t\t\t\t\tпродажам",
                "name": "Ірина",
                "compensation": None,
                "age": 35,
                "location": "Чернівці",
            },
            {
                "cv_url": "https://www.work.ua/resumes/7638972/",
                "position": "Менеджер по\n\t\t\t\t\t\t\t\t\t\t\tобработке\n\t\t\t\t\t\t\t\t\t\t\tзаказов",
                "name": "Аліна",
                "compensation": "13000 грн",
                "age": 18,
                "location": "Чернівці",
            },
        ]

        result = work_ua_candidates_parser.parse(html_content=html_candidates_page_2, url=None)

        assert result.page_number == 1
        assert len(result.candidates) == 14

        actual_candidates: list[dict[str, Any]] = result.model_dump()["candidates"]
        for exp_candidate in contains_expected_candidates:
            assert exp_candidate in actual_candidates
