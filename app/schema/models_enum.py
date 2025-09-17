from enum import StrEnum


class GptModelEnum(StrEnum):
    gpt5 = "gpt-5"
    gpt5mini = "gpt-5-mini"
    gpt5nano = "gpt-5-nano"
    gpt41 = "gpt-4.1"
    gpt41mini = "gpt-4.1-mini"
    gpt41nano = "gpt-4.1-nano"


class ZhipuAIModelEnum(StrEnum):
    glm45v = "glm-4.5v"
    glm45 = "glm-4.5"
    glm45x = "glm-4.5-x"
    glm45air = "glm-4.5-air"
    glm45airx = "glm-4.5-airx"
    glm45flash = "glm-4.5-flash"


class DeepSeekModelEnum(StrEnum):
    deepseek_chat = "deepseek-chat"
    deepseek_reasoner = "deepseek-reasoner"


class QwenModelEnum(StrEnum):
    q4km_gguf = "q4_k_m.gguf"


class GeminiModelEnum(StrEnum):
    gemini_25_flash = "gemini-2.5-flash"
    gemini_25_flash_lite = "gemini-2.5-flash-lite"
    gemini_25_pro = "gemini-2.5-pro"
