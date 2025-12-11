import json
import logging
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from app.schema.chat import ChatParamsCommon, RcBaseMessage, RoleEnum
from app.ai_models.chat import get_chat_model


async def chat(params: ChatParamsCommon):
    """
    通用聊天接口，用于调用模型进行对话，或者调用模型进行总结等操作
    """
    model = get_chat_model(
        model=params.model,
        api_key=params.api_key,
        base_url=params.base_url,
        temperature=params.temperature,
        max_tokens=params.max_tokens,
        # stream=params.streaming,
    )

    # 过滤掉消息列表内的system角色（防止通过messages参数篡改system）
    messages = [
        RcBaseMessage(role=RoleEnum.system, content=params.sys_prompt, turn=None)
    ] + [msg for msg in params.messages if msg.role != RoleEnum.system]

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


async def chat_base(params: ChatParamsCommon):
    """
    基础的聊天接口，用于调用LLM，不支持流式处理
    """
    model = get_chat_model(
        model=params.model,
        api_key=params.api_key,
        base_url=params.base_url,
        temperature=params.temperature,
        max_tokens=params.max_tokens,
    )

    # 过滤掉消息列表内的system角色（防止通过messages参数篡改system）
    messages = [
        RcBaseMessage(role=RoleEnum.system, content=params.sys_prompt, turn=None)
    ] + [msg for msg in params.messages if msg.role != RoleEnum.system]

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

    content = await model.ainvoke(input_data)

    return content.content


if __name__ == "__main__":
    pass
