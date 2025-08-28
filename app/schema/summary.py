from typing import TypedDict
from enum import Enum


class SummarySearchModeEnum(str, Enum):
    keyword = "keyword"
    similarity = "similarity"
    hybrid = "hybrid"


class SummaryDataModel(TypedDict):
    summary: str
    turn: int | None


class SummarySearchResult(TypedDict):
    uuid: str
    summary: str
    turn: int | None
    distance: float | None
    score: float | None
    created_at: str | None
    updated_at: str | None


class SummaryMemory(TypedDict):
    summary: str
    turn: int | None


class TenantInfo(TypedDict):
    name: str
    data_count: int
    activityStatus: str
