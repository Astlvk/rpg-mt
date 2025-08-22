import logging
from fastapi import APIRouter, HTTPException
from sse_starlette import EventSourceResponse
from app.schema.chat import ChatParamsCommon, ChatParamsWriter, ChatParamsSummary
from app.modules.chat.common import chat
from app.modules.chat.writer import chat_writer
from app.modules.chat.summary import chat_summarize

router = APIRouter()


@router.post("/common", summary="通用的模型对话接口，目前支持openai与智谱AI提供的模型")
async def chat_common(data: ChatParamsCommon):
    aiter = chat(data)
    return EventSourceResponse(aiter)


@router.post("/writer", summary="剧情写作接口")
async def chat_writer_api(data: ChatParamsWriter):
    aiter = chat_writer(data)
    return EventSourceResponse(aiter)


@router.post("/summary", summary="剧情摘要接口")
async def chat_summary_api(data: ChatParamsSummary):
    try:
        res = await chat_summarize(data)
        return {"message": "剧情摘要成功", "data": res}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"剧情摘要失败: {str(e)}")
