import abc
from typing import Any

from app.common.schemas.candidates_result import CandidatesPageResultSchema


class BaseAsyncExecutor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def run(self, position: str, **kwargs: Any) -> list[CandidatesPageResultSchema]:
        ...
