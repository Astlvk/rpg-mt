import json
from uuid import UUID
from langchain_core.prompts import ChatPromptTemplate
from app.schema.chat import ChatParamsSummary, RcBaseMessage, RoleEnum
from app.modules.vector_db.summary_repo import SummaryTenantRepo
from .common import chat_base
from app.schema.summary import SummaryDataModel, MergedSummary


async def chat_summarize(params: ChatParamsSummary):
    """
    摘要函数，用于总结对话内容，并向量化到向量库中
    """
    messages = [
        RcBaseMessage(
            role=RoleEnum.user, content=params.summary_prompt, turn=params.turn
        ),
    ] + params.messages

    # # 如果存在系统提示词则拼接到消息列表中
    # if params.summary_system_prompt:
    #     # messages = [
    #     #     RcBaseMessage(
    #     #         role=RoleEnum.system,
    #     #         content=params.summary_system_prompt,
    #     #         turn=None,
    #     #     )
    #     # ] + messages
    #     params.sys_prompt = params.summary_system_prompt

    params.messages = messages

    content = await chat_base(params)

    if isinstance(content, str):
        return await _update_summary(params, content)
    else:
        raise ValueError("summary content is not a string")


async def _update_summary(params: ChatParamsSummary, new_summary: str):
    # 更新摘要
    # 使用content做相似性搜索
    # 如果搜索出摘要，使用llm合并content与历史摘要
    # 如果搜索不出摘要，直接添加到摘要库中
    repo = SummaryTenantRepo(params.tenant_name)

    cur_summary = new_summary
    merged_uuids: list[UUID] = []
    merged_summary: list[MergedSummary] | None = None

    if params.update_summary:
        print("搜索相似摘要====================", params.summary_distance)
        # 搜索相似摘要
        res = await repo.similarity_search(
            cur_summary,
            distance=params.summary_distance,
            top_k=params.summary_top_k,
        )

        # 存在相似摘要，则使用llm合并新摘要与历史摘要
        if res.objects:
            # 相似摘要列表
            similarity_summaries: list[MergedSummary] = []

            for item in res.objects:
                merged_uuids.append(item.uuid)
                similarity_summaries.append(
                    {
                        "summary": item.properties["summary"],
                        "turn": item.properties["turn"],
                    }
                )

            summaries_jsonl = _to_jsonl(similarity_summaries)
            # 获取提示词模板
            prompt_template = ChatPromptTemplate.from_template(
                params.summary_merge_prompt
            )
            # 生成提示词，注入相似摘要列表与新摘要
            msg = prompt_template.invoke(
                {"summaries": summaries_jsonl, "new_summary": cur_summary}
            )
            print(msg.to_string())
            # 合并后的摘要列表，用于持久化保存至当前摘要信息中
            merged_summary = similarity_summaries + [
                {
                    "summary": cur_summary,
                    "turn": params.turn,
                }
            ]
            params.messages = [
                RcBaseMessage(
                    role=RoleEnum.user,
                    content=msg.to_string(),
                    turn=params.turn,
                ),
            ]
            if params.summary_merge_system_prompt:
                params.messages = [
                    RcBaseMessage(
                        role=RoleEnum.system,
                        content=params.summary_merge_system_prompt,
                        turn=None,
                    ),
                ] + params.messages
            cur_summary = await chat_base(params)

    id = await repo.add_summary(
        str(cur_summary), turn=params.turn, merged_summary=merged_summary
    )

    # 删除合并的摘要
    if merged_uuids:
        await repo.delete_summary_by_uuids(merged_uuids)

    return {
        "id": str(id),
        "content": cur_summary,
    }


def _to_jsonl(items: list[MergedSummary]) -> str:
    return "\n".join(json.dumps(x, ensure_ascii=False) for x in items)


if __name__ == "__main__":
    pass
