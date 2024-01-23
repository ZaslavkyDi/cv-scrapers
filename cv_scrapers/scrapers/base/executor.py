import abc
from typing import Any

from cv_common_library.schemas.cv_data_storage.candidates_result import CandidatesPageResultSchema


class BaseAsyncExecutor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def run(self, position: str, **kwargs: Any) -> list[CandidatesPageResultSchema]:
        ...
