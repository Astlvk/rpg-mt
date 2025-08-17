from enum import Enum


class GptModelEnum(str, Enum):
    gpt5 = "gpt-5"
    gpt5mini = "gpt-5-mini"
    gpt5nano = "gpt-5-nano"
    gpt41 = "gpt-4.1"
    gpt41mini = "gpt-4.1-mini"
    gpt41nano = "gpt-4.1-nano"


class ZhipuAIModelEnum(str, Enum):
    glm45v = "glm-4.5v"
    glm45 = "glm-4.5"
    glm45x = "glm-4.5-x"
    glm45air = "glm-4.5-air"
    glm45airx = "glm-4.5-airx"
    glm45flash = "glm-4.5-flash"


class DeviceEnum(str, Enum):
    cpu = "cpu"
    cuda = "cuda"


class EmbeddingModelEnum(str, Enum):
    bge = "bge"
    m3e = "m3e"


class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"
