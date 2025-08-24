from typing import TypedDict
from enum import Enum


class SummarySearchModeEnum(str, Enum):
    keyword = "keyword"
    similarity = "similarity"
    hybrid = "hybrid"


class SummarySearchResult(TypedDict):
    uuid: str
    summary: str
    distance: float | None
    score: float | None
    created_at: str | None
    updated_at: str | None