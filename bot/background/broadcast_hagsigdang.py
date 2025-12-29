import discord
import asyncio
import traceback
from bs4 import BeautifulSoup
from datetime import datetime

from bot.utils.crawler import getText
from bot.utils.database import *
from bot import LOGGER, BOT_NAME_TAG_VER, color_code

async def broadcast_hagsigdang(bot) -> None:
    """ 오늘의 학생식당 메뉴 체크 """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    link = "https://www.kumoh.ac.kr/ko/restaurant01.do"

    while True:
        if datetime.now().weekday() <= 4: # 월 ~ 금
            if datetime.now().hour == 7 and datetime.now().minute == 0:
                result = await getText(link, header)
                parse = BeautifulSoup(result, 'lxml')
                box = parse.find("div", {"class": "menu-list-box"})

                today_menu_list = []
                for i in box.find("tbody").find_all("tr"):
                    menu = i.find_all("td")[datetime.now().weekday()].get_text().strip().split("\n")
                    today_menu_list.append([menu[0], '\n'.join(menu[1:]).strip()])

                await send_hagsigdang(bot, today_menu_list)
        await asyncio.sleep(60)

async def send_hagsigdang(bot, today_menu: list) -> None:
    """ 학생식당 메뉴 전송 """
    
    # 데이터 없으면 안보냄
    if len(today_menu) <= 0:
        return

    # 채널 아이디 리스트 가져오기
    channel_id_list = channelDataDB().get_on_channel("Hagsigdang")
    if channel_id_list is not None and today_menu is not None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed = discord.Embed(title="오늘의 학생식당 메뉴", description='', color=color_code)

                for menu in today_menu:
                    menu_title, menu_content = menu
                    embed.add_field(name=menu_title, value=menu_content, inline=True)

                embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)

            except Exception:
                LOGGER.error(traceback.format_exc())