"""

ID, BoardID, title, author

"""

import sqlite3

from bot import se_db_path, channel_db_path

class seBoardDB():
    def __init__(self):
        self.db_path = se_db_path

    def set_database(self, tr_list: list) -> None:
        """ 데이터베이스에 데이터 추가 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        # Create table if it doesn't exist
        c.execute(f"CREATE TABLE IF NOT EXISTS seboard (id integer PRIMARY KEY AUTOINCREMENT, boardid int, title text, author text)")

        # add se board data
        for tr in tr_list:
            board_id = tr[0]
            title = tr[1].replace("'", "''")
            author = tr[2].replace("'", "''")
            
            try:
                c.execute("SELECT * FROM seboard WHERE boardid=:Id", {"Id": board_id})
                temp = c.fetchone()
            except:
                temp = None
            if temp is None:
                c.execute(f"INSERT INTO seboard (boardid, title, author) VALUES(?, ?, ?)", (board_id, title, author))
        conn.close()

    def get_database(self) -> list | None:
        """ 모든 데이터베이스 가져오기 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM seboard ORDER BY id")
        except:
            conn.close()
            return None
        temp = c.fetchall()
        conn.close()
        return temp
    
    def get_database_from_id(self, id) -> tuple | None:
        """ id로 데이터베이스 가져오기 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM seboard WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_latest_data_id(self) -> int | None:
        """ 마지막 행 id 리턴 """
        all_db = seBoardDB().get_database()
        if all_db is None:
            return None
        else:
            return all_db[-1][0]

class KumohSquareDB():
    def __init__(self):
        # 기존 DB에 테이블 얹어서 사용
        # id, postid, link, category, title, author
        self.db_path = se_db_path

    def set_database(self, tr_list: list) -> None:
        """ 데이터베이스에 데이터 추가 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        # Create table if it doesn't exist
        c.execute(f"CREATE TABLE IF NOT EXISTS seboard (id integer PRIMARY KEY AUTOINCREMENT, boardid int, title text, author text)")

        # add se board data
        for tr in tr_list:
            board_id = tr[0]
            title = tr[1].replace("'", "''")
            author = tr[2].replace("'", "''")
            
            try:
                c.execute("SELECT * FROM seboard WHERE boardid=:Id", {"Id": board_id})
                temp = c.fetchone()
            except:
                temp = None
            if temp is None:
                c.execute(f"INSERT INTO seboard (boardid, title, author) VALUES(?, ?, ?)", (board_id, title, author))
        conn.close()

    def get_database(self) -> list | None:
        """ 모든 데이터베이스 가져오기 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM seboard ORDER BY id")
        except:
            conn.close()
            return None
        temp = c.fetchall()
        conn.close()
        return temp
    
    def get_database_from_id(self, id) -> tuple | None:
        """ id로 데이터베이스 가져오기 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM seboard WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_latest_data_id(self) -> int | None:
        """ 마지막 행 id 리턴 """
        all_db = seBoardDB().get_database()
        if all_db is None:
            return None
        else:
            return all_db[-1][0]

class channelDataDB():
    def __init__(self):
        self.db_path = channel_db_path

    def channel_status_set(self, id: int, status: str) -> None:
        """ 채널 알림설정 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        # Create table if it doesn't exist
        c.execute(f"CREATE TABLE IF NOT EXISTS broadcastChannel (id integer PRIMARY KEY, onoff text)")
        try:
            c.execute("SELECT * FROM broadcastChannel WHERE id=:id", {"id": id})
            a = c.fetchone()
        except:
            a = None
        if a is None:
            # add channel set
            c.execute(f"INSERT INTO broadcastChannel VALUES(?, ?)", (id, status))
        else:
            # modify channel set
            c.execute("UPDATE broadcastChannel SET onoff=:onoff WHERE id=:id", {"onoff": status, 'id': id})
        conn.close()
    
    def get_on_channel(self) -> list | None:
        """ 모든 알람설정 되어있는 채널 가져오기 """
        conn = sqlite3.connect(self.db_path, isolation_level=None)
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
    seBoardDB().set_database(post_list)