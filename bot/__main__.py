import discord
import asyncio

from discord.ext import commands
from bot.background.read_se import read_se
from bot.background.broadcast import broadcast
from bot.background.read_kumoh import read_kumoh
from bot.background.broadcast_kumoh import broadcast_kumoh
# from bot.background.schedule import schedule
from bot.background.broadcast_hagsigdang import broadcast_hagsigdang
from bot.background.broadcast_dormitory import broadcast_dorm_food

from bot import LOGGER, TOKEN, EXTENSIONS, BOT_NAME_TAG_VER

async def status_task():
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game ("/help : 도움말"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity = discord.Game (f"{len(bot.guilds)}개의 서버에 참여하고 있어요!"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
        except Exception:
            pass

class Bot (commands.Bot):
    def __init__ (self):
        super().__init__(
            intents=intents
        )
        self.remove_command("help")

        for i in EXTENSIONS:
            self.load_extension("bot.cogs." + i)

    async def on_ready(self):
        LOGGER.info(BOT_NAME_TAG_VER)
        await self.change_presence(
            activity = discord.Game ("/help : 도움말"),
            status = discord.Status.online,
        )
        
        while background_list != {}:
            module_name = list(background_list.keys())[0]
            pass_variable = background_list.pop(module_name)

            if pass_variable:
                bot.loop.create_task(globals()[module_name](bot))
            else:
                bot.loop.create_task(globals()[module_name]())

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

background_list = {
    "status_task": False,
    "broadcast": True,
    "broadcast_kumoh": True,
    "read_se": False,
    "read_kumoh": False,
    # "schedule": True,
    "broadcast_hagsigdang": True,
    "broadcast_dormitory": True
}

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = Bot()
bot.run(TOKEN)