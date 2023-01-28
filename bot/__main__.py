import discord
import asyncio

from discord.ext import commands
from bot.background.read_se import read_se
from bot.background.broadcast import broadcast
from bot.utils.database import channelDataDB

from bot import LOGGER, TOKEN, EXTENSIONS, BOT_NAME_TAG_VER

async def status_task():
    channel_db = channelDataDB()
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game ("/help : 도움말"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
            channel_list = channel_db.get_on_channel()
            if channel_list is not None:
                await bot.change_presence(
                    activity = discord.Game (f"{len(channel_list)}개의 채널에 알림을 보내주고 있어요!"),
                    status = discord.Status.online,
                )
            await asyncio.sleep(10)
        except Exception:
            pass

class Bot (commands.Bot) :
    def __init__ (self) :
        super().__init__ (
            intents=intents
        )
        self.remove_command("help")

        for i in EXTENSIONS :
            self.load_extension("bot.cogs." + i)

    async def on_ready (self) :
        LOGGER.info(BOT_NAME_TAG_VER)
        await self.change_presence(
            activity = discord.Game ("/help : 도움말"),
            status = discord.Status.online,
        )
        bot.loop.create_task(status_task())
        bot.loop.create_task(broadcast(bot))
        bot.loop.create_task(read_se())

    async def on_message (self, message) :
        if message.author.bot:
            return
        await self.process_commands (message)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = Bot ()
bot.run(TOKEN)