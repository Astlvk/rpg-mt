from enum import Enum


class DeviceEnum(str, Enum):
    cpu = "cpu"
    cuda = "cuda"


class EmbeddingModelEnum(str, Enum):
    bge = "bge"
    m3e = "m3e"


class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"
