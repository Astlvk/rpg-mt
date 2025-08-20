from typing import List
from pydantic import BaseModel, Field
from .message import RoleEnum, RcBaseMessage
from .base import GptModelEnum, ZhipuAIModelEnum


class ChatParamsCommon(BaseModel):
    """通用的chat model参数模型，用于支持多个平台模型入参"""

    model: GptModelEnum | ZhipuAIModelEnum = Field(
        default=ZhipuAIModelEnum.glm45flash,
        description="模型名称，目前支持openai与智谱AI提供的模型",
        examples=[ZhipuAIModelEnum.glm45flash],
    )
    sys_prompt: str = Field(
        default="你是一个乐于助人的智能助理。",
        description="系统提示词",
        examples=["你是一个乐于助人的智能助理。"],
    )
    messages: List[RcBaseMessage] = Field(
        description="消息列表",
        examples=[
            [
                # {"role": RoleEnum.system, "content": "你是一个乐于助人的智能助理。"},
                {"role": RoleEnum.assistant, "content": "你好，有什么可以帮助你的？"},
                {"role": RoleEnum.user, "content": "你好，我想了解下AI发展。"},
            ]
        ],
    )
    temperature: float = Field(
        default=0.9, description="模型温度，取值0.0 ~ 1.0，智谱模型该参数不支持取0或1"
    )
    max_tokens: int = Field(default=65536, description="最大令牌数", examples=[65536])
    streaming: bool = Field(default=True, description="是否启用流式处理")
    # stop: List[str] = []
    # presence_penalty: int = 0
    # frequency_penalty: int = 0


class ChatParamsWriter(ChatParamsCommon):
    """剧情写作接口的参数模型，继承自ChatParamsCommon"""

    instruction_prompt: str = Field(
        default="",
        description="剧情写作的指令，用于指导模型生成剧情",
        examples=["请根据以下剧情，生成一个剧情"],
    )

    summary_prompt: str = Field(
        default="",
        description="摘要提示词，用于指导模型生成摘要",
        examples=["请根据以下剧情，生成一个摘要"],
    )
