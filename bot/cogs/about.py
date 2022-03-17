import discord
from discord.ext import commands
from discord.commands import slash_command

from bot import LOGGER, BOT_NAME_TAG_VER, color_code

class About (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def about (self, ctx) :
        """ 봇에 대한 소개 """
        embed=discord.Embed(title="봇 정보", description="그저 SE 게시판 매번 확인하는게 귀찮았을뿐", color=color_code)
        embed.add_field(name="개발자", value="금오공과대학교 컴퓨터소프트웨어공학과 22학번 새내기", inline=True)
        embed.add_field(name="관련 링크", value="[Github](https://github.com/ajb3296/SE-Board-alarm)\n[SE Board](http://se.kumoh.ac.kr/)", inline=True)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')