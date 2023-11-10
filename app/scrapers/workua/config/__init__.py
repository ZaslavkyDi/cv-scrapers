from functools import lru_cache

from app.scrapers.workua.config.settings import WorkUAScraperSettings


@lru_cache
def get_workua_settings() -> WorkUAScraperSettings:
    return WorkUAScraperSettings()
