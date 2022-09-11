from pydantic import BaseModel, Extra
from nonebot import get_driver


class Config(BaseModel, extra=Extra.ignore):
    chatrecorder_record_send_msg: bool = True

plugin_config = Config.parse_obj(get_driver().config.dict())