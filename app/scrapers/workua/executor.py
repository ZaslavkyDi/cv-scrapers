from typing import Any

import httpx

from app.common.schemas.candidates_result import CandidatesPageResultSchema
from app.scrapers.base.executor import BaseAsyncExecutor
from app.scrapers.workua.parsers import WorkUACandidatesHtmlParser
from app.scrapers.workua.scraper import WorkUACandidatesScraper


class WorkUAExecutor(BaseAsyncExecutor):
    async def run(self, position: str, **kwargs: Any) -> list[CandidatesPageResultSchema]:
        async with httpx.AsyncClient() as client:
            scraper = WorkUACandidatesScraper(
                parser=WorkUACandidatesHtmlParser(),
                httpx_client=client,
            )
            result: list[CandidatesPageResultSchema] = await scraper.scrape(position)
            return result
