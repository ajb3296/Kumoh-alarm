import re
import asyncio
from bs4 import BeautifulSoup

from bot.utils.crawler import getText

async def read_se():
    while True:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        se_board_link = "http://se.kumoh.ac.kr/"
        result = await getText(se_board_link, header)
        #result = requests.get(se_board_link)
        parse = BeautifulSoup(result.text, 'lxml')
        trs = parse.find("table", {"summary" : "List of Articles"}).find("tbody").find_all("tr")
        tr_list = []
        for tr in trs:
            try:
                class_check = tr["class"]
            except:
                tr_list.append((int(re.sub(r'[^0-9]', '', tr.find("td", {"class" : "title"}).find("a")["href"])), tr.find("td", {"class" : "title"}).text.replace("\n", ""), tr.find("td", {"class" : "author"}).text))
            else:
                pass

        await asyncio.sleep(10)

if __name__ == "__main__":
    import requests
    read_se()