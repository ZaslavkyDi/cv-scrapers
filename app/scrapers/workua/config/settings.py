from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkUAScraperSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="workua_")

    host: HttpUrl = "https://www.work.ua"

    @property
    def search_url(self) -> str:
        return f"{self.host}/resumes/?search="
