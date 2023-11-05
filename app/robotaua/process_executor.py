import httpx

from app.common.schemas.candidates_result import CandidatesPageResultSchema
from app.robotaua.parsers import RobotaUACandidatesJsonParser
from app.robotaua.scraper import RobotaUACandidatesScraper


class RobotaUAExecutor:

    async def run(self, position: str) -> None:
        async with httpx.AsyncClient() as client:
            scraper = RobotaUACandidatesScraper(
                parser=RobotaUACandidatesJsonParser(),
                httpx_client=client,
            )
            result: list[CandidatesPageResultSchema] = await scraper.scrape(position)
            print(len(result))
            print(result[-1])
