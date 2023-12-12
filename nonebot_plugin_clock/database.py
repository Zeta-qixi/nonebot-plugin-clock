import os
import sqlite3
from nonebot.log import logger
from pathlib import Path

TABLE = "CLOCKS"
path = Path('./static/clocks')
if not os.path.exists(path):
    os.mkdir(path)
db_ = path.joinpath('data.sqlite')
logger.info(f"CLOCK DB: {db_}")

if not os.path.exists(db_):
    
    conn = sqlite3.connect(db_)

    c = conn.cursor()
    try:
        c.execute(f'''CREATE TABLE {TABLE}(  
            id INTEGER NOT NULL primary key autoincrement,
            type CHAR(10),
            group_id VARCHAR(20),
            user_id VARCHAR(20) NOT NULL,
            content VARCHAR(20),
            month INTEGER,
            day INTEGER,
            week VARCHAR(7),
            c_time TIME,
            ones INTEGER NOT NULL);
        ''')
        logger.info('create db')
    except Exception as e:
        logger.error(repr(e))
        logger.error('create db fail ...')

    conn.commit()
    conn.close()
    

class DB:
    def __init__(self, db, table):
        self.db = db
        self.table = table
        

    def execute(self, sql:str):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        res = c.execute(sql)
        res = list(res)
        conn.commit()
        conn.close()
        return res


    def add_clock(self, clock):
        sql = f'''INSERT INTO {self.table} (id, type, group_id, user_id, content, month, day, week, c_time, ones)
        values ({clock.id}, "{clock.type}", "{clock.group_id}", {clock.user_id}, "{clock.content}","{clock.month}","{clock.day}","{clock.week}","{clock.time}",{clock.ones});'''
        self.execute(sql)


    def del_clock(self, id: int):  
        self.execute(f"DELETE from {self.table} where id = {id}")
        return True


    def select_all(self):
        '''
        (id, type, user_id, content, c_time, ones) 
        '''
        return self.execute(f"SELECT * FROM {self.table};")
    

    def select_by_user(self, id, gid, uid):
        return self.execute(f"SELECT * FROM {self.table} where id = {id} and group_id = {gid} adn user_id = {uid};")

        
    def new_id(self):
        res = self.execute(f"SELECT max(id) FROM {self.table};")
        return res[0][0] + 1 if res[0][0] else 1


db = DB(db_, TABLE)
