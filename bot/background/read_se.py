import re
import asyncio
import traceback
from bs4 import BeautifulSoup

from bot.utils.crawler import getText
from bot.utils.database import seBoardDB
from bot import se_board_link, LOGGER

async def read_se():
    """ SE게시판 새 글 읽기 """
    while True:
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            result = await getText(se_board_link, header)

            parse = BeautifulSoup(result, 'lxml')
            trs = parse.find("table", {"summary": "List of Articles"})

            if trs is not None:
                trs = trs.find("tbody").find_all("tr")
            tr_list = []
        except:
            print(traceback.format_exc())
        else:
            if trs is not None:
                for tr in trs:
                    try:
                        class_check = tr["class"]
                    except:
                        # 클래스가 없는 경우 - 공지가 아닐 경우
                        tr_list.append(
                            (
                                int(re.sub(r'[^0-9]', '', tr.find("td", {"class": "title"}).find("a")["href"])), # 글 번호
                                tr.find("td", {"class": "title"}).text.replace("\n", ""), # 제목
                                tr.find("td", {"class": "author"}).text # 작성자
                            )
                        )
                    else:
                        pass
                
                tr_list.sort(key=lambda x:x[0])

                while True:
                    try:
                        seBoardDB().set_database(tr_list)
                    except:
                        print(traceback.format_exc())
                    else:
                        break

        await asyncio.sleep(60)