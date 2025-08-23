from enum import Enum


class SummarySearchModeEnum(str, Enum):
    keyword = "keyword"
    similarity = "similarity"
    hybrid = "hybrid"

