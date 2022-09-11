from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class MessageRecord(SQLModel, table=True):
    """消息记录"""

    __tablename__: str = "Rechatrecorder_message_record"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    event_name: str
    """
    消息来源
    存放消息的来源的类型
    """
    time: datetime
    """ 
    消息时间
    存放 UTC 时间
    """
    message_type: str
    """
    消息类型
    存放消息的类型
    """
    detail_type:str
    """
    详细消息来源
    """
    message_id: str
    """
    消息id
    存放消息的id
    """
    message: str
    """ 
    消息内容
    存放 onebot 消息段的字符串
    """
    alt_message: str
    """ 
    消息内容的替代表示
    存放纯文本消息
    """
    session_id: Optional[str] = None
    """
    会话id
    包括用户id和群组id
    """
