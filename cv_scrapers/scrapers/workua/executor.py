from typing import Any

import httpx

from cv_scrapers.common.schemas.candidates_result import CandidatesPageResultSchema
from cv_scrapers.scrapers.base.executor import BaseAsyncExecutor
from cv_scrapers.scrapers.workua.parsers import WorkUACandidatesHtmlParser
from cv_scrapers.scrapers.workua.scraper import WorkUACandidatesScraper


class WorkUAExecutor(BaseAsyncExecutor):
    """
    WorkUAExecutor is a class that runs the scraping process for the WorkUA website.

    Example:
        runner = WorkUAExecutor()
        await runner.run(position="адміністратор")
    """
    async def run(self, position: str, **kwargs: Any) -> list[CandidatesPageResultSchema]:
        async with httpx.AsyncClient() as client:
            scraper = WorkUACandidatesScraper(
                parser=WorkUACandidatesHtmlParser(),
                httpx_client=client,
            )
            result: list[CandidatesPageResultSchema] = await scraper.scrape(position)
            return result
