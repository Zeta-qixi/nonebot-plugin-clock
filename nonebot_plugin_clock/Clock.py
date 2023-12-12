import datetime

from nonebot.adapters.qq import  MessageSegment, ActionFailed
from nonebot import get_bot, require
from .database import db

scheduler = require('nonebot_plugin_apscheduler').scheduler

class Clock:
    def __init__(self, data):
 
        self.id = data['id']
        self.type = data.get('type', 'private')
        self.group_id = data.get('group_id')
        self.user_id = data.get('user_id')
        self.content = data.get('content', '')
        self.ones = int(data.get('ones', 1))
        self.month = int(data.get('month', 0))
        self.day = int(data.get('day', 0))
        self.week = str(data.get('week', ''))
        self.time = data.get('time', 1)
        self.get_time()

    @classmethod
    def init_from_db(cls, *args):
        args = args[0]
        data = {}
        data['id'] = args[0]
        data['type'] = args[1]
        data['group_id'] = args[2]
        data['user_id'] = args[3]
        data['content'] = args[4]
        data['month'] = args[5]
        data['day'] = args[6]
        data['week'] = args[7]
        data['time'] = args[8]
        data['ones'] = args[9]
        return cls(data)
    

    def get_info(self):
        ones=['重复', '不重复']
        time_ = ' '.join([i for i in self.time.split() if i !='null'])

        if self.month and self.day:
            tag = f"{self.month}.{self.day}"
        else:
            tag = f'每周{self.week}' if self.week else ones[(self.ones)]
      
        return f'[{self.id}] ⏰{time_} ({tag})\n备注: {self.content}'


    def get_time(self):
        time = self.time.split()[-1].split(':')
        self.hour = int(time[0])
        self.minute = int(time[1])


    def verify_today(self):

        if self.week and str(datetime.date.today().weekday()+1) not in self.week:
            return False
        if self.month > 0 and self.month != datetime.date.today().month:
            return False
        if self.day > 0 and self.day != datetime.date.today().day:
            return False
        return True


def _del_clock(id: int):
    scheduler.remove_job(f"clock_{id}")
    db.del_clock(id)


def del_clock(id: int, gid: str = '', uid: str = ''):
    if db.select_by_user(id, gid, uid):
        _del_clock(id)


def add_clock(**kwargs):
    kwargs['id'] = db.new_id()
    clock = Clock((kwargs))
    db.add_clock(clock)
    _add_to_scheduler(clock)


def get_clock():
    return [Clock.init_from_db(i) for i in db.select_all()]

def _add_to_scheduler(clock):
    """ create clock """
  
    async def _add_clock():
        if clock.verify_today():
            try:
                if clock.type == 'dms':
                    await get_bot().send_to_dms(guild_id=clock.group_id,
                                                message = clock.content)
                else:
                    await get_bot().send_to_channel(channel_id=clock.group_id, 
                                                    message =clock.content)
            except ActionFailed:
                ...
            finally:
                if clock.ones == 1:
                    _del_clock(clock.id)
    scheduler.add_job(_add_clock, "cron", hour=clock.hour, minute=clock.minute, id=f"clock_{clock.id}")


for i in db.select_all():
    _add_to_scheduler(Clock.init_from_db(i))