from typing import List
from pydantic import BaseModel, Field
from .base import GptModelEnum, ZhipuAIModelEnum, EmbeddingModelEnum, SortOrderEnum
from .message import RcBaseMessage, RoleEnum


class QaParams(BaseModel):
    model: GptModelEnum | ZhipuAIModelEnum = Field(
        default=ZhipuAIModelEnum.glm3t,
        description="模型名称，目前支持openai与智谱AI提供的模型",
    )
    temperature: float = Field(
        default=0.01, description="模型温度，0.0 ~ 1.0，智谱模型不支持0和1"
    )
    streaming: bool = Field(default=True, description="是否启用流式处理")
    embedding: EmbeddingModelEnum = Field(
        default=EmbeddingModelEnum.bge,
        description="嵌入模型，默认bge",
        examples=[EmbeddingModelEnum.bge, EmbeddingModelEnum.m3e],
    )
    kb_name: str = Field(..., description="知识库名称", examples=["KB"])
    top_k: int = Field(default=3, description="从知识库检索多少条数据", examples=[3])
    distance: float | None = Field(
        default=None,
        description="知识库检索的相似度阈值，分数越低越相似",
        examples=[None],
    )
    reference_sort: SortOrderEnum | None = Field(
        default=None,
        description="引用数据的排序方式，可根据distance进行升序或降序，null为不排序",
        examples=[None],
    )
    ref_temp: str = Field(
        default="<data>\n{q}\n{a}\n</data>",
        description="引用数据的模板，{q}-检索内容，{a}-预期内容，{d}-相似度（距离）",
        examples=["<data>\n{q}\n{a}\n</data>"],
    )
    prompt_temp: str = Field(
        default='使用 <data></data> 标记中的内容作为你的知识:\n\n{ref_temp}\n\n回答要求：\n- 如果你不清楚答案，你需要澄清。\n- 避免提及你是从 <data></data> 获取的知识。\n- 保持答案与 <data></data> 中描述的一致。\n- 使用 Markdown 语法优化回答格式。\n- 使用与问题相同的语言回答。\n\n问题:"""{question}"""',
        description="提示词模板，{ref_temp}-由ref_temp生成的引用数据，{question}-用户的输入（问题）",
        examples=[
            '使用 <data></data> 标记中的内容作为你的知识:\n\n{ref_temp}\n\n回答要求：\n- 如果你不清楚答案，你需要澄清。\n- 避免提及你是从 <data></data> 获取的知识。\n- 保持答案与 <data></data> 中描述的一致。\n- 使用 Markdown 语法优化回答格式。\n- 使用与问题相同的语言回答。\n\n问题:"""{question}"""'
        ],
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
                {"role": RoleEnum.assistant, "content": "你好，有什么可以帮助你的？"},
                {"role": RoleEnum.user, "content": "你好，我想了解下AI发展。"},
            ]
        ],
    )
    agent_mode: bool = Field(
        default=False,
        description="是否启用agent模式，agent模式会由llm自动判断是否查询知识库。",
        examples=[True, False],
    )
