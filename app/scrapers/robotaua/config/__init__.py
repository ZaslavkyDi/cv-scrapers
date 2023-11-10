from functools import lru_cache

from app.scrapers.robotaua.config.settings import RobotaUAScraperSettings


@lru_cache
def get_robotaua_settings() -> RobotaUAScraperSettings:
    return RobotaUAScraperSettings()
