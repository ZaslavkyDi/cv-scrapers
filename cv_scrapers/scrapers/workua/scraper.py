import asyncio
import dataclasses
import logging
from collections.abc import Awaitable
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from cv_scrapers.common.schemas.candidates_result import CandidatesPageResultSchema
from cv_scrapers.scrapers.exceptions import NoLastPageNumber
from cv_scrapers.scrapers.workua.config import get_workua_settings
from cv_scrapers.scrapers.workua.parsers import WorkUACandidatesHtmlParser

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class FirstPageResult:
    page_result: CandidatesPageResultSchema
    last_page_number: int


class WorkUACandidatesScraper:
    HOST: str = str(get_workua_settings().host)

    def __init__(self, parser: WorkUACandidatesHtmlParser, httpx_client: AsyncClient) -> None:
        self._parser = parser
        self._httpx_client = httpx_client

    async def scrape(self, position_title: str) -> list[CandidatesPageResultSchema]:
        search_response = await self._get_url_by_position_response(title=position_title)

        if not search_response.next_request:
            raise ValueError("Can not find positions URL for candidates.")

        base_position_url = search_response.next_request.url

        first_page_result: FirstPageResult = await self._scrape_first_page(
            base_url=base_position_url
        )
        last_page_number = first_page_result.last_page_number
        candidates_pages_result = [first_page_result.page_result]

        if last_page_number == 1:
            return candidates_pages_result

        coros: list[Awaitable[CandidatesPageResultSchema]] = []
        for page_number in range(2, last_page_number + 1):
            coros.append(self.scrape_page(base_url=base_position_url, page_number=page_number))

        coro_result = await asyncio.gather(*coros)
        candidates_pages_result.extend(coro_result)

        return candidates_pages_result

    async def scrape_page(self, base_url: str, page_number: int) -> CandidatesPageResultSchema:
        url = f"{base_url}?page={page_number}"
        response: Response = await self._httpx_client.get(url)
        response.raise_for_status()

        return self._parser.parse(
            html_content=response.text,
            url=url,
        )

    async def _get_url_by_position_response(self, title: str) -> Response:
        url: str = f"{get_workua_settings().search_url}{title}&region=57"  # Chernivtsi = 57
        response: Response = await self._httpx_client.get(url)

        if response.status_code >= 400:
            response.raise_for_status()
        return response

    async def _scrape_first_page(self, base_url: str) -> FirstPageResult:
        url = urljoin(base_url, "/?page=1")
        response: Response = await self._httpx_client.get(url)
        response.raise_for_status()

        content = response.text
        page_result = self._parser.parse(
            html_content=content,
            url=url,
        )
        try:
            last_page_number = self._parser.parse_last_page_number(
                content=content,
                url=url,
            )
        except NoLastPageNumber:
            logger.info(f"Can not find last page number for {url}. Set last page number to 1.")
            last_page_number = 1

        return FirstPageResult(page_result=page_result, last_page_number=last_page_number)
