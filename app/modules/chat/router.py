from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from app.schema.chat import ChatParamsCommon
from app.modules.chat.common import chat

router = APIRouter()


@router.post("/common", summary="通用的模型对话接口，目前支持openai与智谱AI提供的模型")
async def chat_common(data: ChatParamsCommon):
    aiter = chat(data)
    return EventSourceResponse(aiter)
