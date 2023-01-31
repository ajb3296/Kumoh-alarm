import re
import asyncio
import traceback
from bs4 import BeautifulSoup

from bot.utils.crawler import getText
from bot.utils.database import KumohSquareDB
from bot import kumoh_square_link, LOGGER, KumohSquarePage

async def read_kumoh():
    """ 금오광장 새 글 읽기 """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    while True:
        for i in KumohSquarePage:
            try:
                # 링크 생성
                link = kumoh_square_link + i.value
                result = await getText(link, header)

                parse = BeautifulSoup(result, 'lxml')
                trs = parse.find("div", {"class": "board-list01"})

                if trs is not None:
                    trs = trs.find("tbody").find_all("tr")
                tr_list = []
            except:
                print(traceback.format_exc())
            else:
                if trs is not None:
                    for tr in trs:
                        # 클래스가 notice 가 아닐 경우
                        if tr["class"] == []:
                            # 링크 가져오기
                            post_link = link + tr.find("td", {"class": "title left"}).find("a")["href"]

                            # 링크에서 글 번호 가져오기
                            post_num = re.search(r"&articleNo=([0-9]+)&", post_link)
                            if post_num is not None:
                                post_num = int(post_num.group(1))
                            tr_list.append(
                                (
                                    i.name, # 게시판 이름
                                    post_num, # 글 번호
                                    post_link, # 링크
                                    tr.find("td", {"class": "category"}).text.strip(), # 카테고리
                                    tr.find("span", {"class": "title-wrapper"}).text.strip(), # 제목
                                    tr.find("td", {"class": "writer"}).text.strip() # 작성자
                                )
                            )

                    while True:
                        try:
                            KumohSquareDB().set_database(tr_list)
                        except:
                            print(traceback.format_exc())
                        else:
                            break

        await asyncio.sleep(60)