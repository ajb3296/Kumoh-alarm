import discord
from discord.ext import commands
from discord.commands import slash_command, Option

from bot.utils.database import channelDataDB
from bot import LOGGER, BOT_NAME_TAG_VER, color_code

class AlarmSet (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def alarmset (self, ctx, onoff : Option(str, "이 채널에서의 알람을 켜거나 끕니다", choices=["ON", "OFF"])) :
        """ 채널에서 SE Board 알림을 켜거나 끕니다 """
        onoff = onoff.lower
        await channelDataDB.channel_status_set(onoff)

        if onoff == "on":
            msg_title = "이 채널에서 알람을 켰습니다"
        else:
            msg_title = "이 채널에서 알람을 껐습니다"
        embed=discord.Embed(title=msg_title, description=f"", color=color_code)

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (AlarmSet (bot))
    LOGGER.info('AlarmSet loaded!')