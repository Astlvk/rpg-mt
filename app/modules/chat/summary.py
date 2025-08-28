from typing import TypedDict
from dataclasses import dataclass
from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from app.schema.chat import ChatParamsSummary, RcBaseMessage, RoleEnum
from app.modules.vector_db.summary_repo import SummaryTenantRepo
from .common import chat_base


async def chat_summarize(params: ChatParamsSummary):
    """
    摘要函数，用于总结对话内容，并向量化到向量库中
    """
    messages = params.messages + [
        RcBaseMessage(role=RoleEnum.user, content=params.summary_prompt),
    ]
    params.messages = messages
    content = await chat_base(params)
    # TODO: 摘要合并
    # 使用content做相似性搜索，距离设置0.3
    # 如果搜索出摘要，使用llm合并content与历史摘要
    # 如果搜索不出摘要，直接添加到摘要库中
    # 参数扩展：
    # 1. 是否开启更新
    # 2. distance
    # 3. 合并用提示词
    await update_summary(params, content)

    repo = SummaryTenantRepo(params.tenant_name)
    if isinstance(content, str):
        id = await repo.add_summary(content, turn=params.turn)
        return {
            "id": str(id),
            "content": content,
        }
    else:
        raise ValueError("summary content is not a string")

async def update_summary(params: ChatParamsSummary, new_summary: str):
    # TODO: 更新摘要
    pass