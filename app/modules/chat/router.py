import logging
from fastapi import APIRouter, HTTPException
from sse_starlette import EventSourceResponse
from app.schema.chat import ChatParamsCommon, ChatParamsWriter, ChatParamsSummary
from app.modules.chat.common import chat, chat_base
from app.modules.chat.writer import chat_writer, WriterAgent
from app.modules.chat.summary import chat_summarize

router = APIRouter()


@router.post("/common", summary="通用的模型对话接口，目前支持openai与智谱AI提供的模型")
async def chat_common_api(data: ChatParamsCommon):
    aiter = chat(data)
    return EventSourceResponse(aiter)


@router.post(
    "/base", summary="基础对话接口，非流式（streaming参数无效），用于支持一次性内容生成"
)
async def chat_base_api(data: ChatParamsCommon):
    """
    基础对话接口，适用于简单的对话场景。
    """
    try:
        res = await chat_base(data)
        return {"message": "success", "data": res}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"基础对话失败: {str(e)}")


@router.post("/writer", summary="剧情写作接口")
async def chat_writer_api(data: ChatParamsWriter):
    aiter = chat_writer(data)
    return EventSourceResponse(aiter)


@router.post("/writer-agent", summary="剧情写作接口（使用agent）")
async def chat_writer_agent_api(data: ChatParamsWriter):
    agent = WriterAgent(data)
    aiter = agent.run()
    return EventSourceResponse(aiter)


@router.post("/summary", summary="剧情摘要接口")
async def chat_summary_api(data: ChatParamsSummary):
    try:
        res = await chat_summarize(data)
        return {"message": "剧情摘要成功", "data": res}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"剧情摘要失败: {str(e)}")
