import re
from datetime import datetime, timedelta
from nonebot.adapters.qq.event import GuildMessageEvent, DirectMessageCreateEvent

def get_event_info( event: GuildMessageEvent ):
        """
        Return (type gid uid)
        """
        if isinstance(event, DirectMessageCreateEvent):
            return ('dms', event.guild_id, event.get_user_id()) # type: ignore
        else:
            return ('channel', event.channel_id, event.get_user_id()) # type: ignore
            



def get_time(time_):
    """
    获取指定时间字符串的标准化时间格式
    Args:
        time_ (str): 输入的时间字符串，可以为 "+2H30M"（表示2小时30分钟后的时间） 或 "13:45"（指定的具体时间）
    
    Returns:
        str: 标准化的时间格式字符串，例如 "13:45"
    """
    t = None
    r = re.match(r'(\d+)[:|\-|：|.](\d+)',time_)
    if time_.startswith('+'):
        h = re.search(r"(\d+)[Hh时]",time_)
        m = re.search(r"(\d+)[Mm分]",time_)
        h=int(h.groups()[0]) if h else 0
        m=int(m.groups()[0]) if m else 0
        t = (datetime.now() + timedelta(hours=h, minutes=m)).strftime("%H:%M")

    elif r:
        h, m = r.groups()
        if int(h) < 24 or int(m) < 60:
            h = f'0{h}' if len(h)==1 else h
            m = f'0{m}' if len(m)==1 else m
            t = f'{h}:{m}'

    return t
        