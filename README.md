# 2023.3.19 已废弃!!!

## 由于本插件的宿主插件已经更新对频道的支持,本插件不再使用

#

#

#

# nonebot-plugin-chatrecorder

适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的聊天记录插件。

## 安装

- 使用 nb-cli

```cmd
nb plugin install nonebot_plugin_chatrecorder
```

- 使用 pip

```cmd
pip install nonebot_plugin_chatrecorder
```

## 配置

插件不会记录机器人收到的消息，可以开启协议端自身消息上报

插件依赖 [nonebot-plugin-datastore](https://github.com/he0119/nonebot-plugin-datastore) 插件

消息记录文件存放在 nonebot-plugin-datastore 插件设置的数据目录；同时插件会将消息中 base64 形式的图片、语音等存成文件，放置在 nonebot-plugin-datastore 插件设置的缓存目录，避免消息记录文件体积过大

## 使用

示例：

```python
from datetime import datetime, timedelta
from nonebot_plugin_chatrecorder import get_message_records
from nonebot.adapters.onebot.v11 import GroupMessageEvent

@matcher.handle()
def handle(event: GroupMessageEvent):
    # 获取当前群114514内成员 '1919810' 和 '54321' 1天之内的消息
    msgs = await get_message_records(
        session_ids=['group_114514_1919810', 'group_114514_54321']
        time_start=datetime.utcnow() - timedelta(days=1),
    )
```

我知道用session_ids获取整个群的消息会异常的烦(),所以等我想到更好的解决方案前建议还是这么用着()

如果真的觉得烦可以通过.record.get_group_all_user(gid:int,bot:Bot)直接获得一个QQ群的人的id

详细参数及说明见代码注释

## TODO

- 修改session_id为分布的group_id和user_id,让get_message_records用起来更方便?

## 感谢

本插件是根据插件[nonebot-plugin-chatrecorder](https://github.com/he0119/nonebot-plugin-chatrecorder) 重写修改而来的
