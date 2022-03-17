import sqlite3

from bot import se_db_path, channel_db_path

class seBoardDB:
    async def set_database(tr_list: list):
        # Create table if it doesn't exist
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS seboard (id integer PRIMARY KEY, title text, author int)")

        latest_data_id = await seBoardDB.get_latest_data_id()
        if latest_data_id is None:
            latest_data_id = tr_list[0][0]

        # add se board data
        for tr in tr_list:
            if tr[0] > latest_data_id:
                c.execute(f"INSERT INTO seboard VALUES{tr}")
        conn.close()
    
    async def get_database():
        # 모든 데이터베이스 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM seboard ORDER BY id")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()
        return temp
    
    async def get_database_from_id(id):
        # id로 데이터베이스 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM seboard WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    async def get_latest_data_id():
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM seboard ORDER BY id DESC LIMIT 1;")
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp[0]

class channelDataDB:
    async def channel_status_set(id: int, status: str):
        # Create table if it doesn't exist
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS broadcastChannel (id integer PRIMARY KEY, onoff text)")
        c.execute("SELECT * FROM userdata WHERE id=:id", {"id": id})
        a = c.fetchone()
        if a is None:
            # add channel set
            c.execute(f"INSERT INTO channel VALUES('{id}', '{status}')")
        else:
            # modify channel set
            c.execute("UPDATE channel SET onoff=:onoff WHERE id=:id", {"onoff": status, 'id': id})
        conn.close()
    
    async def get_on_channel():
        # 모든 알람설정 되어있는 채널 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM channel ORDER BY id")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()

        on_channel = []
        for channel in temp:
            if temp[1] == "on":
                on_channel.append(channel[0])
        return on_channel