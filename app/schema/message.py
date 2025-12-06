from enum import Enum
from pydantic import BaseModel, Field


class RoleEnum(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class History(BaseModel):
    """
    历史消息
    """

    role: RoleEnum = Field(..., description="角色")
    content: str = Field(..., description="消息内容")


class RcBaseMessage(BaseModel):
    """
    基础消息类型，区别于langchain提供的BaseMessage
    """

    role: RoleEnum = Field(..., description="角色")
    content: str = Field(..., description="消息内容")
    turn: int | None = Field(
        None, description="可选的，对话轮次，用于记录消息的产生回合，对应前端的turn"
    )
