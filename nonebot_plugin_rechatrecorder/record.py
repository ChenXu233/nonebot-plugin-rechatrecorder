from datetime import datetime
from sqlmodel import select, or_
from typing_extensions import Literal
from typing import Iterable, List, Optional, Union, overload

from nonebot.adapters import Bot
from nonebot_plugin_datastore import create_session

from .model import MessageRecord
from .config import plugin_config as pc 

async def get_group_all_user(gid:int,bot:Bot)->List[str]:
    all_uesr = await bot.call_api("get_group_member_list",group_id=gid,no_cache=True)
    out = []
    for i in all_uesr:
        out.append('group_{}_{}'.format(gid,i["user_id"]))
    return out
    

@overload
async def get_message_records(
    plain_text: Literal[True],
    event_names: Optional[Iterable[str]] = None,
    session_ids: Optional[Iterable[str]] = None,
    exclude_event_names: Optional[Iterable[str]] = None,
    exclude_session_ids: Optional[Iterable[str]] = None,
    message_type: Optional[Iterable[str]] = None,
    time_start: Optional[datetime] = None,
    time_stop: Optional[datetime] = None,
) -> List[str]:
    ...


@overload
async def get_message_records(
    plain_text: Literal[False] = ...,
    event_names: Optional[Iterable[str]] = None,
    session_ids: Optional[Iterable[str]] = None,
    exclude_event_names: Optional[Iterable[str]] = None,
    exclude_session_ids: Optional[Iterable[str]] = None,
    message_type: Optional[Iterable[str]] = None,
    time_start: Optional[datetime] = None,
    time_stop: Optional[datetime] = None,
) -> List[MessageRecord]:
    ...


async def get_message_records(
    plain_text: bool = False,
    event_names: Optional[Iterable[str]] = None,
    session_ids: Optional[Iterable[str]] = None,
    exclude_event_names: Optional[Iterable[str]] = None,
    exclude_session_ids: Optional[Iterable[str]] = None,
    message_type: Optional[Iterable[str]] = None,
    time_start: Optional[datetime] = None,
    time_stop: Optional[datetime] = None,
) -> Union[List[str], List[MessageRecord]]:
    """
    :说明:

      获取消息记录

    :参数:

      * ``plain_text: bool = False``: 为真则返回字符串数组，否则返回 MessageRecord 数组
      * ``platforms: Optional[Iterable[str]]``: 平台列表，为空表示所有平台
      * ``session_ids: Optional[Iterable[str]]``: 群组列表，为空表示所有群组
      * ``exclude_platforms: Optional[Iterable[str]]``: 不包含的平台列表，为空表示不限制
      * ``exclude_session_ids: Optional[Iterable[str]]``: 不包含的群组列表，为空表示不限制
      * ``message_type: Optional[Iterable[str]]``: 包含的消息类型，为空表示所有类型
      * ``time_start: Optional[datetime]``: 起始时间，UTC 时间，为空表示不限制起始时间
      * ``time_stop: Optional[datetime]``: 结束时间，UTC 时间，为空表示不限制结束时间

    :返回值:

      * ``Union[List[str], List[MessageRecord]]``: 消息列表
    """

    whereclause = []
    if session_ids:
        whereclause.append(
            or_(*[MessageRecord.session_id == session_id for session_id in session_ids]) # type: ignore
        )
    if event_names:
        whereclause.append(
            or_(*[MessageRecord.event_name == event_name for event_name in event_names]) # type: ignore
        )
    if exclude_session_ids:
        for session_id in exclude_session_ids:
            whereclause.append(MessageRecord.session_id != session_id)
    if exclude_event_names:
        for exclude_event_name in exclude_event_names:
            whereclause.append(MessageRecord.event_name != exclude_event_name)
    if message_type:
        whereclause.append(MessageRecord.detail_type == message_type)
    if time_start:
        whereclause.append(MessageRecord.time >= time_start)
    if time_stop:
        whereclause.append(MessageRecord.time <= time_stop)

    statement = select(MessageRecord).where(*whereclause)
    async with create_session() as session:
        records: List[MessageRecord] = (await session.exec(statement)).all() # type: ignore

    if plain_text:
        return [record.alt_message for record in records]
    else:
        return records
    
    
# TODO: 内置消息处理方法
class MessageRecordProcesser():
    """
    提供对从数据库获得的消息的处理
    """
    def __init__(self,records:List[MessageRecord]):
        self.records = records
    
    async def get_message_from_alt_message_on_keyword(self):
        """
        从一堆MessageRecord对象中找出带有有关键字的消息
        返回 带有关键字消息的MessageRecord数组
        """
        pass
    
    async def get_message_num_on_group(self):
        """
        按组计算消息量
        返回 键为组的ID,值为数字的字典
        """
        pass
    
    async def get_message_num_on_user_id(self):
        """
        按用户计算消息量
        返回 键位用户ID,值为数字的字典
        """
        pass
    
    