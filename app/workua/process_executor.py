import asyncio
import multiprocessing

import httpx

from app.workua.parsers import WorkUACandidatesHtmlParser
from app.workua.schemas.schemas import CandidatesPageResultSchema
from app.workua.scraper import WorkUACandidatesScraper


class WorkUAExecutor:

    async def run(self, position: str) -> None:
        async with httpx.AsyncClient() as client:
            scraper = WorkUACandidatesScraper(
                parser=WorkUACandidatesHtmlParser(),
                httpx_client=client,
            )
            result: list[CandidatesPageResultSchema] = await scraper.scrape(position)
            print(len(result))
            print(result[-1])
