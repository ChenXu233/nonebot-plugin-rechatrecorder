from datetime import datetime

from nonebot import  require
from nonebot.adapters import Event
from nonebot.message import event_postprocessor

require("nonebot_plugin_datastore")
from nonebot_plugin_datastore import create_session

from .model import MessageRecord
from .config import plugin_config as pc
from .message import *
from .record import *


@event_postprocessor
async def record_recv_msg(event: Event):
    """
    在所有消息后处理消息到数据库
    """
    
    #发神经段，建议是不要学（
    try:
        time = datetime.utcfromtimestamp(event.time)  # type: ignore
    except AttributeError:
        time = datetime.utcnow()
    try:
        detail_type = event.message_type  # type: ignore
    except AttributeError:
        detail_type = 'UNKOWN'
    try:
        message_id = event.message_id  # type: ignore
    except AttributeError:
        message_id = 'Null'
    try:
        session_id = event.get_session_id()
    except NotImplementedError:
        session_id = None
    except ValueError:
        return
    try:
        alt_message = event.get_plaintext()
    except ValueError:
        alt_message = ''
        
    record = MessageRecord(
        event_name=event.get_event_name(),
        time=time, 
        message_type=event.get_type(),
        detail_type=detail_type,
        message_id=message_id,
        message=str(event.get_event_description()),
        alt_message=alt_message,
        session_id=session_id,
    )

    async with create_session() as session:
        session.add(record)
        await session.commit()


# async def record_send_msg(
#     bot: BaseBot,
#     e: Optional[Exception],
#     api: str,
#     data: Dict[str, Any],
#     result: Optional[Dict[str, Any]],
# ):

#     if e or not result:
#         return
#     if api not in ["send_msg", "send_private_msg", "send_group_msg"]:
#         return

#     message = Message(data["message"])
#     record = MessageRecord(
#         platform="qq",
#         time=datetime.utcnow(),
#         type="message",
#         detail_type="group"
#         if api == "send_group_msg"
#         or (api == "send_msg" and data["message_type"] == "group")
#         else "private",
#         message_id=str(result["message_id"]),
#         message=serialize_message(message),
#         alt_message=message.extract_plain_text(),
#         user_id=str(bot.self_id),
#         group_id=str(data.get("group_id", "")),
#     )

#     async with create_session() as session:
#         session.add(record)
#         await session.commit()


# plugin_config = Config.parse_obj(get_driver().config.dict())
# if plugin_config.chatrecorder_record_send_msg:
#     Bot.on_called_api(record_send_msg)

"""
    你问我为什么留怎么长一段注释?
    当然为了证明这个插件是从大佬MeetWq的插件chatrecorder改的()
    虽然如此，你是不是觉得我有点大病?
    确实有，前面的trytrytry你也看见咯
    而且我也懒的一批，删这玩意的功夫不如写彩蛋(doge)
    
    如果你看了被注释掉的部分，可能会问我为什么不实现这个功能
    这是因为这个功能可以通过打开机器人自己消息上报的选项开启来解决
    我懒得写这个()
    如果写了的话这个彩蛋也许就不在了?
    这也许不是彩蛋,就是占用储存的()
    因为一个中文占俩个字节!!(doge)
    
    最后再次感谢大佬MeetWq首先写出插件chatrecorder(虽然他咕了,但不影响我prpr大佬())
"""