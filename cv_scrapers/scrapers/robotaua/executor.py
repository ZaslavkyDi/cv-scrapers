from typing import Any

import httpx

from cv_scrapers.common.schemas.candidates_result import CandidatesPageResultSchema
from cv_scrapers.scrapers.base.executor import BaseAsyncExecutor
from cv_scrapers.scrapers.robotaua.parsers import RobotaUACandidatesJsonParser
from cv_scrapers.scrapers.robotaua.scraper import RobotaUACandidatesScraper


class RobotaUAExecutor(BaseAsyncExecutor):
    """
    RobotaUAExecutor is a class that runs the scraping process for the RobotaUA website.

    Example:
        runner = WorkUAExecutor()
        await runner.run(position="адміністратор")
    """

    async def run(self, position: str, **kwargs: Any) -> list[CandidatesPageResultSchema]:
        async with httpx.AsyncClient() as client:
            scraper = RobotaUACandidatesScraper(
                parser=RobotaUACandidatesJsonParser(),
                httpx_client=client,
            )
            result: list[CandidatesPageResultSchema] = await scraper.scrape(position)
            return result
