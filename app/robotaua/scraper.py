import asyncio
import dataclasses
import math
from collections.abc import Awaitable

from httpx import AsyncClient, Response

from app.common.schemas.candidates_result import CandidatesPageResultSchema
from app.robotaua.config import get_robotaua_settings
from app.robotaua.config.enums import CityId
from app.robotaua.parsers import RobotaUACandidatesJsonParser
from app.robotaua.schemas.request import ResumeSearchRequestPayload
from app.workua.config import get_workua_settings


@dataclasses.dataclass
class FirstPageResult:
    page_result: CandidatesPageResultSchema
    total_items: int
    request_step: int


class RobotaUACandidatesScraper:

    RESUME_SEARCH_URL: str = str(get_robotaua_settings().search_url)

    def __init__(
        self,
        parser: RobotaUACandidatesJsonParser,
        httpx_client: AsyncClient
    ) -> None:
        self._parser = parser
        self._httpx_client = httpx_client

    async def scrape(self, position_title: str) -> list[CandidatesPageResultSchema]:
        first_page_result: FirstPageResult = await self._scrape_first_page(position_title)
        last_page_number = self._calculate_last_page_number(
            total_items=first_page_result.total_items,
            step=first_page_result.request_step,
        )
        candidates_pages_result = [first_page_result.page_result]

        if last_page_number == 0:
            return candidates_pages_result

        coros: list[Awaitable[CandidatesPageResultSchema]] = []
        for page_number in range(1, last_page_number):
            coros.append(
                self.scrape_page(
                    position=position_title,
                    page_number=page_number
                )
            )

        coro_result = await asyncio.gather(*coros)
        candidates_pages_result.extend(coro_result)

        return candidates_pages_result

    async def scrape_page(self, position: str, page_number: int) -> CandidatesPageResultSchema:
        payload = self._build_request_payload(
            position=position,
            page_number=page_number,
        )
        response: Response = await self._httpx_client.post(
            url=self.RESUME_SEARCH_URL,
            json=payload.model_dump(by_alias=True),
        )
        response.raise_for_status()

        return self._parser.parse(
            json_content=response.text,
            page_number=page_number
        )

    async def _scrape_first_page(self, position: str) -> FirstPageResult:
        page_number = 0

        payload = self._build_request_payload(
            position=position,
            page_number=page_number,
        )
        response: Response = await self._httpx_client.post(
            url=self.RESUME_SEARCH_URL,
            json=payload.model_dump(by_alias=True),
        )
        response.raise_for_status()

        content: str = response.text
        page_result = self._parser.parse(
            json_content=content,
            page_number=page_number,
        )

        return FirstPageResult(
            page_result=page_result,
            total_items=self._parser.parse_total_resumes_number(content),
            request_step=self._parser.parse_resume_request_step(content),
        )

    @staticmethod
    def _build_request_payload(position: str, page_number: int) -> ResumeSearchRequestPayload:
        return ResumeSearchRequestPayload(
            key_words=position,
            page=page_number,
            city_id=CityId.CHERNIVTSI.value,
        )

    @staticmethod
    def _calculate_last_page_number(total_items: int, step: int) -> int:
        result = total_items / step
        if result < 1:
            return 0

        return math.ceil(total_items / step)
