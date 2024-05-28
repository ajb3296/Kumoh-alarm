import re
import asyncio
import requests
import traceback

# from bot.utils.crawler import getText
from bot.utils.database import seBoardDB
from bot import se_board_link, LOGGER

async def read_se():
    """ SE게시판 새 글 읽기 """
    se_link = f"{se_board_link}v1/posts?categoryId=1&page=0&perPage=20"
    while True:
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            result = requests.get(se_link, headers=header).json()  # 해당 링크의 html 코드를 가져옴
            content_li = result["content"]

            result_list = []

            if content_li is not None:
                for content in content_li:

                    login_id = str(content["author"]["userId"])
                    if login_id is None:
                        login_id = "익명"

                    result_list.append(
                        (
                            content["postId"], # 글 번호
                            content["title"].replace("\n", ""), # 제목
                            content["author"]["name"], # 작성자 이름
                            login_id # 작성자 아이디
                        )
                    )

                result_list.sort(key=lambda x:x[0])

                while True:
                    try:
                        seBoardDB().set_database(result_list)
                    except:
                        print(traceback.format_exc())
                    else:
                        break
        
        except:
            print(traceback.format_exc())
        await asyncio.sleep(60)