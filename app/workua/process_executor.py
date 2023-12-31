import httpx

from app.common.schemas.candidates_result import CandidatesPageResultSchema
from app.workua.parsers import WorkUACandidatesHtmlParser
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
