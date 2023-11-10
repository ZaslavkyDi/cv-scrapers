from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class RobotaUAScraperSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="robotaua_")

    api_host: HttpUrl = "https://employer-api.robota.ua"

    @property
    def search_url(self) -> str:
        return f"{self.api_host}cvdb/resumes"

    @property
    def resume_url_template(self) -> str:
        return "https://robota.ua/candidates/{resume_id}"
