from typing import TypedDict, NotRequired
from enum import Enum


class SummarySearchModeEnum(str, Enum):
    keyword = "keyword"
    similarity = "similarity"
    hybrid = "hybrid"


class SummaryTypeEnum(str, Enum):
    character = "character"
    summary = "summary"
    other = "other"


class MergedSummary(TypedDict):
    summary: str
    turn: int | None


class SummaryDataModel(TypedDict):
    summary: str
    turn: int | None
    type: SummaryTypeEnum | None
    merged_summary: list[MergedSummary] | None


class SummaryDataModelUpdate(TypedDict):
    summary: str
    turn: int | None
    type: SummaryTypeEnum | None


class SummarySearchResult(TypedDict):
    uuid: str
    summary: str
    turn: int | None
    type: str | None
    merged_summary: list[MergedSummary] | None
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
