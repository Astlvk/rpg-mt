import json
import logging
from typing import cast
from langchain.messages import HumanMessage, SystemMessage, AIMessage, AIMessageChunk
from langchain.tools import tool
from langchain.agents import create_agent
from app.schema.chat import ChatParamsWriter, RcBaseMessage, RoleEnum
from app.schema.summary import SummaryMemory
from app.ai_models.chat import get_chat_model
from app.modules.vector_db.summary_repo import SummaryTenantRepo
from .tools import deep_think


class WriterAgent:
    def __init__(self, params: ChatParamsWriter):
        self.docs = []
        self.params = params
        self.model = get_chat_model(
            model=params.model,
            api_key=params.api_key,
            base_url=params.base_url,
            temperature=params.temperature,
            max_tokens=params.max_tokens,
            # extra_body={
            #     "thinking": {
            #         "type": "enabled",
            #     },
            # },
        )
        # 如果启用记忆检索，则添加记忆检索工具
        tools = (
            [deep_think] + [self.query_memory_wrap()]
            if self.params.enable_retriever
            else []
        )
        self.agent = create_agent(
            model=self.model,
            tools=tools,
            system_prompt=self.params.sys_prompt,
            debug=False,
        )

    async def run(self):
        # 过滤掉消息列表内的system角色（防止通过messages参数篡改system）
        messages = [msg for msg in self.params.messages if msg.role != RoleEnum.system]

        # 如果存在instruction_prompt，则添加到messages中
        if self.params.instruction_prompt:
            messages.append(
                RcBaseMessage(
                    role=RoleEnum.user, content=self.params.instruction_prompt
                )
            )

        # 需要把messages转换为BaseMessage
        input_data = [
            (
                # SystemMessage(content=message.content)
                {"role": "system", "content": message.content}
                if message.role == RoleEnum.system
                else (
                    # AIMessage(content=message.content)
                    {"role": "assistant", "content": message.content}
                    if message.role == RoleEnum.assistant
                    else (
                        # HumanMessage(content=message.content)
                        {"role": "user", "content": message.content}
                    )
                )
            )
            for message in messages
        ]

        try:
            if self.params.streaming:
                aiter = self.agent.astream(
                    {"messages": [*input_data]},
                    stream_mode="messages",
                )
                async for item, metadata in aiter:
                    if isinstance(item, AIMessageChunk):
                        # print(item)

                        usage_metadata = item.usage_metadata

                        if usage_metadata:
                            usage_metadata = {
                                "inputTokens": usage_metadata["input_tokens"],
                                "outputTokens": usage_metadata["output_tokens"],
                                "totalTokens": usage_metadata["total_tokens"],
                            }

                        yield json.dumps(
                            {
                                "content": item.content,
                                "usageMetadata": usage_metadata,
                            },
                            ensure_ascii=False,
                        )
                    else:
                        # yield item
                        print("function_call================================")
                        print(item)
                # 流式返回检索到的摘要
                yield json.dumps({"docs": self.docs}, ensure_ascii=False)
                self.docs = []
            else:
                content = await self.agent.ainvoke(
                    {"messages": [*input_data]},
                    stream_mode="messages",
                )
                # print(content)
                content = cast(list[AIMessageChunk], content)
                ai_text = "".join(
                    str(item.content)
                    for item in content
                    if isinstance(item, AIMessageChunk)
                )
                yield json.dumps({"content": ai_text}, ensure_ascii=False)
        except Exception as e:
            logging.exception(e)
            msg = repr(e)
            yield json.dumps(
                {"content": f"网络错误，请稍后重试。error: {msg}"}, ensure_ascii=False
            )

    def query_memory_wrap(self):
        # 额外的工具描述，提供则使用
        desc = self.params.query_tool_prompt or None

        @tool(parse_docstring=True, description=desc)
        async def query_memory(querys: list[str]):
            """
            查询历史记忆，使用相似性搜索检索与用户对话相关的记忆（历史摘要）。

            Args:
                querys: 查询内容，用于检索与用户对话相关的记忆（历史摘要），可以传入多个查询内容。

            Returns:
                list[str]: 查询到的记忆（历史摘要）JSON字符串格式, summary为摘要内容， turn=n表示第n轮记忆。
            """
            print(f"查询记忆: {querys}")
            try:
                repo = SummaryTenantRepo(self.params.tenant_name)
                res_summaries: list[SummaryMemory] = []

                for query in querys:
                    res = await repo.summary_search(
                        query=query,
                        mode=self.params.retriever_mode,
                        distance=self.params.distance,
                        top_k=self.params.top_k,
                    )

                    docs = res["data"]

                    # 保存检索到的摘要，用于流式返回
                    self.docs.append(
                        {
                            "query": query,
                            "summaries": docs,
                        }
                    )

                    # 取出摘要数据
                    summaries: list[SummaryMemory] = [
                        {
                            "summary": summary["summary"],
                            "turn": summary["turn"],
                        }
                        for summary in docs
                    ]

                    res_summaries.extend(summaries)

                # 去重：只保留summary和turn都相同的唯一项
                unique = {}
                for s in res_summaries:
                    key = (s["summary"], s["turn"])
                    if key not in unique:
                        unique[key] = s
                res_summaries = list(unique.values())

                print(f"查询到的记忆: {[s['turn'] for s in res_summaries]}")

                return json.dumps(res_summaries, ensure_ascii=False)
            except Exception as e:
                logging.exception(e)
                return "检索出错！"

        return query_memory


async def chat_writer(params: ChatParamsWriter):
    model = get_chat_model(
        model=params.model,
        api_key=params.api_key,
        base_url=params.base_url,
        temperature=params.temperature,
        max_tokens=params.max_tokens,
        extra_body={
            "thinking": {
                "type": "disabled",
            },
        },
    )

    # 过滤掉消息列表内的system角色（防止通过messages参数篡改system）
    messages = [RcBaseMessage(role=RoleEnum.system, content=params.sys_prompt)] + [
        msg for msg in params.messages if msg.role != RoleEnum.system
    ]

    # 需要把messages转换为BaseMessage
    input_data = [
        (
            SystemMessage(content=message.content)
            if message.role == RoleEnum.system
            else (
                AIMessage(content=message.content)
                if message.role == RoleEnum.assistant
                else HumanMessage(content=message.content)
            )
        )
        for message in messages
    ]

    try:
        if params.streaming:
            aiter = model.astream(input_data)
            async for item in aiter:
                yield json.dumps({"content": item.content}, ensure_ascii=False)
        else:
            content = await model.ainvoke(input_data)
            yield json.dumps({"content": content.content}, ensure_ascii=False)
    except Exception as e:
        logging.exception(e)
        msg = repr(e)
        yield json.dumps(
            {"content": f"网络错误，请稍后重试。error: {msg}"}, ensure_ascii=False
        )


if __name__ == "__main__":
    pass
