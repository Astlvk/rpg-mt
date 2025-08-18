from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from app.schema.chat import ChatParamsCommon, ChatParamsWriter
from app.modules.chat.common import chat
from app.modules.chat.writer import chat_writer

router = APIRouter()


@router.post("/common", summary="通用的模型对话接口，目前支持openai与智谱AI提供的模型")
async def chat_common(data: ChatParamsCommon):
    aiter = chat(data)
    return EventSourceResponse(aiter)


@router.post("/writer", summary="剧情写作接口")
async def chat_writer_api(data: ChatParamsWriter):
    aiter = chat_writer(data)
    return EventSourceResponse(aiter)
