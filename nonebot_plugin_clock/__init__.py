import re

from datetime import datetime, timedelta
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_regex ,get_bot, get_driver, require
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message




from .database import db
from .Clock import Clock

scheduler = require('nonebot_plugin_apscheduler').scheduler

WHITELIST = getattr(get_driver().config, 'clock_white_list', [])
BLACKLIST = getattr(get_driver().config, 'clock_black_list', [])
CLOCK_DATA = {}


del_clock_qq = on_command('删除闹钟', block=True)
add_clock_qq = on_command('添加闹钟', aliases={'设置闹钟',}, block=True)

async def CLOCK_RULE(bot: Bot, event: MessageEvent) -> bool:
    
    ret = await SUPERUSER(bot, event)
    if ret: return True

    # 黑名单优先判定
    if BLACKLIST:
        return event.user_id not in BLACKLIST
    
    if WHITELIST:
        if event.sender.role == "member" and event.user_id not in WHITELIST:
            return False
        
    return True

def get_event_info( event: MessageEvent ):
    if isinstance(event, GroupMessageEvent):
        return ('group', event.group_id)
    else:
        return ('private', event.user_id)

def create_clock_scheduler(clock):
    '''
    创建闹钟任务
    '''
    CLOCK_DATA[clock.id] = clock

    async def add_clock():
        if clock.verify_today():
            await get_bot().send_msg(message_type=clock.type, user_id=clock.user, group_id=clock.user, message=clock.content)          

            if clock.ones == 1:
                del_clock(clock.id, clock.user)

    scheduler.add_job(add_clock, "cron", hour=clock.hour, minute=clock.minute, id=f"clock_{clock.id}")


for i in db.select_all():
    create_clock_scheduler(Clock.init_from_db(i))


def add_clock(**kwargs):
    """添加闹钟"""
    kwargs['id'] = db.new_id()
    clock = Clock((kwargs))
    db.add_clock(clock)
    create_clock_scheduler(clock)

def del_clock(id: int, uid: int):
    """
    删除闹钟 防止用户误删
    Args:
        id(int): database中的clock id (唯一)
        uid(int): user_id 或 group_id
    Returns:
        bool
    """
    if db.del_clock(id, uid):
        del(CLOCK_DATA[id])
        scheduler.remove_job(f"clock_{id}")
        return True



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
        

# 创建闹钟
@add_clock_qq.handle()
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State, messages: Message = CommandArg()):
    
    messages = str(messages).split(' ', 1)

    if len(messages) < 2:
        await matcher.finish(message="添加格式为: “添加闹钟 时间 内容”")

    time_ = get_time(messages[0])
    if not time_:
        await matcher.finish(message="时间格式错误")

    state['time'] = time_
    state['type'], state['user'] = get_event_info(event)
    state['content'] = messages[1] if messages[1] else '⏰'

    if state['type'] == 'group':

        ret = await CLOCK_RULE(bot, event)
        if not ret:
            await matcher.finish(message="你没有该权限哦～")



@add_clock_qq.got('ones', prompt="⏰设置不重复输入[N/n]\n⏰设置为每日输入[Y/y]\n⏰设置周几 如周一周三输入[13]\n⏰设置某天，如圣诞输入 [12.25]")
async def _(matcher: Matcher, state: T_State):

    state['ones'] = str(state['ones'])
    ones = 0 if state['ones'] in ['Y', 'y'] else 1 # Y,y之外的非数字 都设置一次性
    month, day = 0, 0
    week = ''

    if state['ones'].isdigit():
        week = state['ones']
        ones = 0

    elif ret:=re.match(r'([0-9]{0,2})[./]([0-9]{1,2})$', state['ones']):
        month, day = ret.groups()

    data = {
        'user' : state['user'],
        'content' : state['content'],
        'time' : state['time'],
        'type' : state['type'],
        'ones' : ones,
        'week' : week,
        'day' : day,
        'month' : month
    }
       
    add_clock(**data)
    ones_ = {1:'不重复', 0:'重复'}
    await matcher.finish(message=f"[{ones_[ones]}]添加成功～")




# # 查看闹钟
check = on_regex("^(查看闹钟|提醒事项|闹钟|⏰)$" ,block=True)
@check.handle()
async def _(matcher: Matcher, event: MessageEvent):

    _, uid = get_event_info(event)
    def check_(msg: str) -> str:

        message = ""
        for m in Message(msg):
            if m.type == 'at':
                message += f"@{m.data['qq']}"
            else:
                message += str(m)
        return message
    
    clock_msg = []
    for id in CLOCK_DATA:
        clock = CLOCK_DATA[id]
        if clock.user == uid:
            clock_msg.append(check_(clock.get_info()))

    if clock_msg:
        await matcher.finish(message= Message('\n'.join(clock_msg)))
    else:
        await matcher.finish(message='目前没有闹钟')
    


# 删除闹钟
@del_clock_qq.handle()
async def _(matcher: Matcher, event: MessageEvent, ids = CommandArg()):

    _, uid = get_event_info(event)
    task = [[],[]]

    for id in str(ids).split():
        id = int(id)
        if del_clock(id, uid):
            task[0].append(id) # succeed
        else:
            task[1].append(id) # fail
    await matcher.finish(message=f'删除闹钟{task[0]}'+ f'\n不存在的id{task[1]}' if task[1] else '')
