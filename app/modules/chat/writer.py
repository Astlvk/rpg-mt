import json
import logging
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from app.schema.chat import ChatParamsWriter, RcBaseMessage, RoleEnum
from app.ai_models.chat import get_chat_model


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
    input_data: list[BaseMessage] = [
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
