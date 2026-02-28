from .clock import *
from .natural_language_clock import *
from nonebot.plugin import PluginMetadata
from .config import  Config


__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_clock",
    description="QQ机器人智能闹钟插件，支持群聊与私聊提醒、支持图片发送、自然语言设置、多样化时间格式",
    usage="添加闹钟 21:00 | 查看闹钟 | 删除闹钟 1 | 每天8点叫我起床",
    config=Config,
)