from enum import StrEnum


class GptModelEnum(StrEnum):
    gpt5 = "gpt-5"
    gpt5mini = "gpt-5-mini"
    gpt5nano = "gpt-5-nano"
    gpt41 = "gpt-4.1"
    gpt41mini = "gpt-4.1-mini"
    gpt41nano = "gpt-4.1-nano"


class DeepSeekModelEnum(StrEnum):
    deepseek_v4_flash = "deepseek-v4-flash"
    deepseek_v4_pro = "deepseek-v4-pro"
