import discord
from discord import option
from discord.ext import commands
from discord.commands import slash_command, Option

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS, KumohSquarePage

class ScheduleAlarmSet (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.table = "Schedule"

    @slash_command()
    @option("onoff", description="이 서버에서의 학사일정 연동을 켜거나 끕니다", choices=["ON", "OFF"])
    async def scheduleset (self, ctx, onoff: str):
        """ 서버에서 학사일정 연동을 켜거나 끕니다 """
        # 오너가 아닐 경우 관리자 권한이 있는지 확인
        if ctx.author.id not in OWNERS:
            if not ctx.author.guild_permissions.manage_messages:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.respond(embed=embed)

        # onoff를 소문자로 변환
        onoff = onoff.lower()
        # 채널 알림 상태를 DB에 저장
        channelDataDB().channel_status_set(self.table, ctx.guild.id, onoff)

        if onoff == "on":
            msg_title = ":green_circle: 이 서버에서 학사일정 연동을 켰습니다"
        else:
            msg_title = ":red_circle: 이 서버에서 학사일정 연동을 껐습니다"
        embed=discord.Embed(title="알람 설정", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)
    
    @slash_command()
    async def schedulestatus (self, ctx):
        """ 이 서버에서 학사일정 연동이 켜져있는지 확인합니다. """
        # 채널 알림 상태를 DB에서 불러옴
        on_guild_list = channelDataDB().get_on_channel(self.table)
        if ctx.guild.id in on_guild_list:
            msg_title = ":green_circle: 이 서버에서 학사일정 연동이 켜져있습니다."
        else:
            msg_title = ":red_circle: 이 서버에서 학사일정 연동이 꺼져있습니다."
        embed=discord.Embed(title="채널 알람 상태", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (ScheduleAlarmSet (bot))
    LOGGER.info('ScheduleAlarmSet loaded!')