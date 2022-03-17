import discord
import asyncio

from bot.utils.database import *
from bot import BOT_NAME_TAG_VER, se_board_link

async def broadcast(bot):
    latest_data_id = await seBoardDB.get_latest_data_id()
    while True:
        now_latest_data_id = await seBoardDB.get_latest_data_id()
        if latest_data_id != latest_data_id:
            for num in range(latest_data_id + 1, now_latest_data_id + 1):
                # get post
                post = await seBoardDB.get_database_from_id(num)
                if post is not None:
                    send_msg(bot, post)

            latest_data_id = now_latest_data_id
            await asyncio.sleep(10)

async def send_msg(bot, post):
    if post[2] in ["이한나[조교]", "오득환", "김선명", "이현아", "김시관", "신윤식", "이해연"]:
        # 빨간색
        color = 0xff0000
        important = "매우 중요"
    elif post[2] in ["학생회"]:
        # 오렌지색
        color = 0xff7f00
        important = "중요"
    else:
        # 초록색
        color = 0x008000
        important = "보통"
    channel_id_list = await channelDataDB.get_on_channel()
    if channel_id_list != None:
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed=discord.Embed(title=post[1], description=f"", color=color)
                embed.add_field(name="글쓴이", value=post[2], inline=True)
                embed.add_field(name="중요도", value=important, inline=True)
                embed.add_field(name="링크", value=f"{se_board_link}freeboard{post[0]}", inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)
            except:
                pass