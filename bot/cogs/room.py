import discord
from discord import option
from discord.ext import commands
from discord.commands import slash_command

import json
import datetime

from bot import LOGGER, BOT_NAME_TAG_VER, color_code
from bot.utils.crawler import getText

class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @option("room", description="프로젝트실을 선택하세요", choices=["D330", "DB134"])
    async def room(self, ctx, room: str):
        """ 현재 프로젝트실 예약이 가능한지 조회합니다 """
        # 방 전체 리스트 가져옴
        room_list = []
        rooms=json.loads(await getText("https://kiosek.kr/api/v1/rooms")).get('result')
        for i in rooms:
            if i["roomName"] == room:
                for j in i.get('projectTableList'):
                    room_list.append(j['tableName'])
                break

        # 조회 시작시간, 종료시간 설정
        start_time = datetime.datetime.now().strftime('%Y%%2F%m%%2F%d+%H:00:00')
        end_time = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime('%Y%%2F%m%%2F%d+%H:00:00')

        # 예약 불가능한 리스트 가져옴
        tableDeactivationList = json.loads(await getText(f"https://kiosek.kr/api/v1/reservations?projectRoomId=3&firstAt={start_time}&lastAt={end_time}")).get('result').get("reservedList")
        if tableDeactivationList is None:
            tableDeactivationList = []
        else:
            tableDeactivationList = [i["tableName"] for i in tableDeactivationList]
        
        
        # 방이 예약가능한지 체크
        for i in tableDeactivationList:
            if i in room_list:
                room_list.remove(i)
        
        # 예약 가능한 방
        reservation_possible = '\n'.join(room_list)
        # 예약 불가능한 방
        reservation_impossible = '\n'.join(tableDeactivationList)
        embed=discord.Embed(title=f"{room} 현황", description="", color=color_code)
        embed.add_field(name="예약 가능", value=reservation_possible, inline=True)
        embed.add_field(name="예약 불가능", value=reservation_impossible, inline=True)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Room(bot))
    LOGGER.info('Room loaded!')