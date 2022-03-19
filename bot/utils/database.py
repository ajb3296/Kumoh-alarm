"""

ID, BoardID, title, author

"""

import sqlite3

from bot import se_db_path, channel_db_path

class seBoardDB:
    def set_database(tr_list: list):
        # Create table if it doesn't exist
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS seboard (id integer PRIMARY KEY AUTOINCREMENT, boardid int, title text, author text)")

        # add se board data
        for tr in tr_list:
            try:
                c.execute("SELECT * FROM seboard WHERE boardid=:Id", {"Id": tr[0]})
                temp = c.fetchone()
            except:
                temp = None
            if temp is None:
                title = tr[1].replace("'", "''")
                c.execute(f"INSERT INTO seboard (boardid, title, author) VALUES({tr[0]}, '{title}', '{tr[2]}')")
        conn.close()

    def get_database():
        # 모든 데이터베이스 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM seboard ORDER BY id")
        except:
            conn.close()
            return None
        temp = c.fetchall()
        conn.close()
        return temp
    
    def get_database_from_id(id):
        # id로 데이터베이스 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM seboard WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_latest_data_id():
        # 마지막 행 id 리턴
        all_db = seBoardDB.get_database()
        if all_db is None:
            return None
        else:
            return all_db[-1][0]

class channelDataDB:
    def channel_status_set(id: int, status: str):
        # Create table if it doesn't exist
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS broadcastChannel (id integer PRIMARY KEY, onoff text)")
        try:
            c.execute("SELECT * FROM broadcastChannel WHERE id=:id", {"id": id})
            a = c.fetchone()
        except:
            a = None
        if a is None:
            # add channel set
            c.execute(f"INSERT INTO broadcastChannel VALUES('{id}', '{status}')")
        else:
            # modify channel set
            c.execute("UPDATE broadcastChannel SET onoff=:onoff WHERE id=:id", {"onoff": status, 'id': id})
        conn.close()
    
    def get_on_channel():
        # 모든 알람설정 되어있는 채널 가져오기
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM broadcastChannel ORDER BY id")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()

        on_channel = []
        for channel in temp:
            if channel[1] == "on":
                on_channel.append(channel[0])
        return on_channel

if __name__ == "__main__":
    se_db_path = "se_board.db"
    channel_db_path = "channel.db"
    post_list = [(80000, '제목1', '글쓴이1'), (80001, '제목2', '글쓴이2')]
    seBoardDB.set_database(post_list)