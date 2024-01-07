from functools import lru_cache

from cv_scrapers.scrapers.robotaua.config.settings import RobotaUAScraperSettings


@lru_cache
def get_robotaua_settings() -> RobotaUAScraperSettings:
    return RobotaUAScraperSettings()
