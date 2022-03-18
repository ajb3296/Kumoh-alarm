import discord
from discord.ext import commands
from discord.commands import slash_command, Option

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code, OWNERS

class AlarmSet (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def alarmset (self, ctx, onoff : Option(str, "이 채널에서의 알람을 켜거나 끕니다", choices=["ON", "OFF"])) :
        """ 채널에서 SE Board 알림을 켜거나 끕니다 """
        if ctx.author.id not in OWNERS:
            if not ctx.message.author.guild_permissions.manage_messages:
                embed=discord.Embed(title="이 명령어는 서버의 관리자만이 사용할 수 있습니다!")
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.respond(embed=embed)
        onoff = onoff.lower()
        channelDataDB.channel_status_set(ctx.channel.id, onoff)

        if onoff == "on":
            msg_title = ":green_circle: 이 채널에서 알람을 켰습니다"
        else:
            msg_title = ":red_circle: 이 채널에서 알람을 껐습니다"
        embed=discord.Embed(title="알람 설정", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)
    
    @slash_command()
    async def alarmstatus (self, ctx) :
        """ 이 채널에서 SE Board 알람이 켜져있는지 확인합니다. """
        on_channel_list = channelDataDB.get_on_channel()
        if ctx.channel.id in on_channel_list:
            msg_title = ":green_circle: 이 채널에서 알람이 켜져있습니다."
        else:
            msg_title = ":red_circle: 이 채널에서 알람이 꺼져있습니다."
        embed=discord.Embed(title="채널 알람 상태", description=msg_title, color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (AlarmSet (bot))
    LOGGER.info('AlarmSet loaded!')