from app.modules.vector_db.summary_repo import SummaryTenantRepo
from app.schema.chat import ChatParamsSummary, RcBaseMessage, RoleEnum
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

    repo = SummaryTenantRepo(params.tenant_name)
    if isinstance(content, str):
        id = await repo.add_summary(content)
        return {
            "id": str(id),
            "content": content,
        }
    else:
        raise ValueError("summary content is not a string")
