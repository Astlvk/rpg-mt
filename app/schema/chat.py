from typing import List
from pydantic import BaseModel, Field, field_validator
from .message import RoleEnum, RcBaseMessage
from .models_enum import (
    GptModelEnum,
    ZhipuAIModelEnum,
    DeepSeekModelEnum,
    QwenModelEnum,
    GeminiModelEnum,
)
from .summary import SummarySearchModeEnum


class ChatParamsCommon(BaseModel):
    """通用的chat model参数模型，用于支持多个平台模型入参"""

    model: (
        GptModelEnum
        | ZhipuAIModelEnum
        | DeepSeekModelEnum
        | QwenModelEnum
        | GeminiModelEnum
    ) = Field(
        default=ZhipuAIModelEnum.glm45flash,
        description="模型名称，目前支持openai与智谱AI提供的模型",
        examples=[ZhipuAIModelEnum.glm45flash],
    )

    api_key: str = Field(
        default="",
        description="API密钥，用于调用模型",
        examples=["4ab6d7e736d8420285d625e23acc30f5.QIJ8mAcCkwfDUym9"],
    )
    base_url: str = Field(
        default="",
        description="API地址，用于调用模型",
        examples=["https://open.bigmodel.cn/api/paas/v4/"],
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

    tenant_name: str = Field(
        ...,
        description="租户名称，用于指定摘要的租户，对应前端的sessionId",
        examples=["sessionId"],
    )

    enable_retriever: bool = Field(
        default=True,
        description="是否启用记忆检索",
        examples=[True],
    )

    retriever_mode: SummarySearchModeEnum = Field(
        default=SummarySearchModeEnum.similarity,
        description="检索方式",
        examples=[SummarySearchModeEnum.similarity],
    )

    distance: float = Field(
        default=0.5,
        description="检索距离",
        examples=[0.5],
    )

    top_k: int = Field(
        default=10,
        description="检索数量",
        examples=[10],
    )

    instruction_prompt: str = Field(
        default="",
        description="剧情写作的指令，用于指导模型生成剧情",
        examples=["请根据对话内容剧情，生成下一段剧情"],
    )

    # summary_prompt: str = Field(
    #     default="",
    #     description="摘要提示词，用于指导模型生成摘要",
    #     examples=["请根据以下剧情，生成一个摘要"],
    # )

    query_tool_prompt: str | None = Field(
        default=None,
        description="检索工具提示词，用于描述提供给LLM的检索工具",
        examples=["请根据剧情，从历史剧情中查询相关内容，用于剧情写作"],
    )


class ChatParamsSummary(ChatParamsCommon):
    """摘要接口的参数模型，继承自ChatParamsCommon"""

    sys_prompt: str = Field(
        default="你是摘要模块的系统提示词。",
        description="摘要用系统提示词，用于指导模型生成摘要",
        examples=[
            "你是一个资深的游戏叙事设计师，擅长提炼故事核心要素。你的任务是将一段游戏对话历史，浓缩成一份结构化的记忆摘要。"
        ],
    )

    summary_prompt: str = Field(
        ...,
        description="摘要提示词，用于指导模型生成摘要",
        examples=["请根据对话内容剧情，生成一个摘要"],
    )

    tenant_name: str = Field(
        ...,
        description="租户名称，用于指定摘要的租户，对应前端的sessionId",
        examples=["sessionId"],
    )

    turn: int | None = Field(
        default=None,
        description="可选的，对话轮次，用于记录摘要的产生的回合，对应前端的turn",
        examples=[None, 0],
    )

    update_summary: bool = Field(
        default=False,
        description="是否启用更新摘要",
        examples=[False],
    )

    summary_distance: float = Field(
        default=0.2,
        description="更新摘要时用于搜索的相似性距离",
        examples=[0.2],
    )

    summary_top_k: int = Field(
        default=5,
        description="更新摘要时用于搜索的摘要数量",
        examples=[5],
    )

    summary_merge_system_prompt: str | None = Field(
        default="",
        description="合并用系统提示词，用于指导模型合并摘要",
        examples=[
            "你是一个专业的剧情档案管理员，负责将关于同一故事的多份摘要报告合并成一份唯一、最新、简洁且结构化的总摘要。"
        ],
    )

    summary_merge_prompt: str = Field(
        default="",
        description="合并提示词，用于指导模型合并摘要",
        examples=["请根据{summarys}历史摘要与{new_summary}新摘要，合并成新的摘要"],
    )
