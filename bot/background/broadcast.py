import os
import discord
import asyncio

from bot.utils.database import *
from bot.utils.preview import get_preview
from bot import LOGGER, BOT_NAME_TAG_VER, se_board_link, se_db_path

async def broadcast(bot):
    if not os.path.exists(se_db_path):
        await asyncio.sleep(5)
    latest_data_id = seBoardDB.get_latest_data_id()
    await asyncio.sleep(5)
    while True:
        now_latest_data_id = seBoardDB.get_latest_data_id()
        if latest_data_id != now_latest_data_id:
            for num in range(latest_data_id + 1, now_latest_data_id + 1):
                # get post
                post = seBoardDB.get_database_from_id(num)
                try:
                    img_preview, preview = await get_preview(post[1])
                except:
                    # 글 수정/삭제되었을 경우 오류 예외처리
                    preview = False
                if post is not None:
                    LOGGER.info(f"Send msg : {post}")
                    await send_msg(bot, post, preview, img_preview)

            latest_data_id = now_latest_data_id
        await asyncio.sleep(60)

async def send_msg(bot, post, preview, img_preview):
    if post[3] in ["오득환", "김선명", "이현아", "김시관", "신윤식", "이해연", "김병만"]:
        # 빨간색
        color = 0xff0000
        important = ":red_circle: 매우 중요"
        everyone_ping = True
    elif post[3] in ["이한나[조교]", "학생회"]:
        # 오렌지색
        color = 0xff7f00
        important = ":orange_circle: 중요"
        everyone_ping = False
    else:
        # 초록색
        color = 0x008000
        important = ":green_circle: 보통"
        everyone_ping = False

    channel_id_list = channelDataDB.get_on_channel()
    if channel_id_list != None:
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                if everyone_ping:
                    await target_channel.send("@everyone")
                embed=discord.Embed(title=post[2], description=f"", color=color)
                embed.add_field(name="글쓴이", value=post[3], inline=True)
                embed.add_field(name="중요도", value=important, inline=True)
                embed.add_field(name="링크", value=f"{se_board_link}freeboard/{post[1]}", inline=False)
                if preview is not False:
                    embed.add_field(name="미리보기", value=preview, inline=False)
                if img_preview is not None:
                    embed.set_image(url=img_preview)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)
            except:
                pass