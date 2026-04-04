import discord
import traceback
import httpx
import asyncio
from datetime import datetime, timedelta

from bot.utils.database import *
from bot import LOGGER, BOT_NAME_TAG_VER, color_code

async def broadcast_employment(bot) -> None:
    """ 오늘의 개발자 채용 정보 """
    url = "https://jasoseol.com/employment/calendar_list.json"
    target_duty = [160, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182]

    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        if now.hour == 7 and now.minute == 0:
            req = {
                "start_time": yesterday_str + "T00:00:00.000Z",
                "end_time": today_str + "T23:59:00.000Z",
            }

            response = httpx.post(url, data=req).json()

            result = []

            for i in response["employment"]:
                # 오늘 시작하는 애들만
                if i["start_time"].split("T")[0] == today_str:
                    # 직무 체크
                    isDevDuty = False
                    for j in i["employments"]:
                        for z in j["duty_groups"]:
                            if z["group_id"] in target_duty:
                                isDevDuty = True
                                break
                        if isDevDuty:
                            break
                    
                    if isDevDuty:
                        result.append(i)

        await asyncio.sleep(60)

async def send_employment(bot, today_employment: list) -> None:
    """ 오늘의 개발자 채용 정보 전송 """
    
    # 데이터 없으면 안보냄
    if len(today_employment) <= 0:
        return

    # 채널 아이디 리스트 가져오기
    channel_id_list = channelDataDB().get_on_channel("Employment")
    if channel_id_list is not None and today_employment is not None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed = discord.Embed(title="오늘 시작하는 개발자 채용 정보", description='', color=color_code)

                for i in today_employment:
                    employment_id = i["id"]
                    company_name = i["name"]
                    employment_title = i["title"]
                    end_date = i["end_date"].split("T")[0]

                    value = f"[{employment_title}](https://jasoseol.com/recruit/{employment_id}) (~{end_date})"

                    embed.add_field(name=company_name, value=value, inline=True)

                embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)

            except Exception:
                LOGGER.error(traceback.format_exc())