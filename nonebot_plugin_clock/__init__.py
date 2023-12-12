import re
from nonebot import on_command, on_regex, logger
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.qq import (Message, GuildMessageEvent)
from .Clock import add_clock, del_clock, get_clock
from .uilts import get_event_info, get_time


del_clock_qq = on_command('删除闹钟', block=True)
add_clock_qq = on_command('添加闹钟', aliases={'设置闹钟',}, block=True)


# 创建闹钟
@add_clock_qq.handle()
async def _(matcher: Matcher, event: GuildMessageEvent, state: T_State, messages: Message = CommandArg()): 
    
    messages = str(messages).split(' ', 1) # type: ignore
    if len(messages) < 2:
        await matcher.finish(message="添加格式为: “添加闹钟 时间 内容”")
    time_ = get_time(messages[0])
    if not time_:
        await matcher.finish(message="时间格式错误")
    state['time'] = time_
    state['type'], state['group_id'] ,state['user_id'] = get_event_info(event)
    state['content'] = messages[1] if messages[1] else '⏰'



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
        'user_id' : state['user_id'],
        'group_id' : state['group_id'],
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
async def _(matcher: Matcher, event: GuildMessageEvent):

    _, gid, uid = get_event_info(event)
    def check_(msg: str) -> str:

        message = ""
        for m in Message(msg):
            if m.type == 'at':
                message += f"@{m.data['qq']}"
            else:
                message += str(m)
        return message
    
    clock_msg = []
    for clock in get_clock():
        if clock.user_id == uid and clock.group_id == gid:
            clock_msg.append(check_(clock.get_info()))

    if clock_msg:
        await matcher.finish(message= Message('\n'.join(clock_msg)))
    else:
        await matcher.finish(message='目前没有闹钟')
    


# 删除闹钟
@del_clock_qq.handle()
async def _(matcher: Matcher, event: GuildMessageEvent, ids = CommandArg()):

    _, gid, uid = get_event_info(event)
    succeed, fail = [], []
    for id in str(ids).split():
        if del_clock(int(id), gid, uid):
            succeed.append(id) # succeed
        else:
            fail.append(id) # fail
    await matcher.finish(message=f'删除闹钟{succeed}'+ f'\n不存在的id{fail}' if fail else 'ok~')
