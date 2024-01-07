import enum


@enum.unique
class ScraperSourceName(enum.StrEnum):
    robotaua = enum.auto()
    workua = enum.auto()
    all = enum.auto()
