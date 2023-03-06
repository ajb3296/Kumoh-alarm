import os
import discord
import asyncio
import traceback

from bot.utils.database import *
from bot.utils.ks_preview import get_ks_preview
from bot import LOGGER, BOT_NAME_TAG_VER, db_path, color_code

async def broadcast_kumoh(bot):
    """ 금오광장 새 글 알림 전송 """
    if not os.path.exists(db_path):
        await asyncio.sleep(5)
    while True:
        latest_data_id = KumohSquareDB().get_all_latest_data_ids()
        # None 이 아닐 경우 반복문 탈출
        if latest_data_id != []:
            break
        # None 일 경우 5초 대기
        await asyncio.sleep(5)
    await asyncio.sleep(5)

    while True:
        # 최신 글 id 가져오기
        while True:
            now_latest_data_id = KumohSquareDB().get_all_latest_data_ids()
            # None 이 아닐 경우 반복문 탈출
            if now_latest_data_id != []:
                break
            # None 일 경우 5초 대기
            await asyncio.sleep(5)

        for data in latest_data_id.items():
            table_name, latest_id = data
            now_id: int = now_latest_data_id[table_name]
            # 최신 글 id 가 변경되었을 경우
            if latest_id != now_id:
                # 데이터 id로 글을 가져와 전송
                for data_id in range(latest_id + 1, now_id + 1):
                    post = KumohSquareDB().get_database_from_id(table_name, data_id)
                    # 데이터베이스에 정보가 존재할 경우
                    if post is not None:
                        link = post[2]

                        img_preview = None
                        preview_text = None
                        try:
                            img_preview, preview_text = await get_ks_preview(link)
                        except:
                            print(traceback.format_exc())

                        # 메시지 전송
                        LOGGER.info(f"Send msg : {post}")
                        await send_msg(bot, table_name, post, preview_text, img_preview)

                latest_data_id = now_latest_data_id
        await asyncio.sleep(60)

async def send_msg(bot, table_name: str, post: tuple, preview: (str | None), img_preview: (str | None)):
    """ 메시지 전송 """
    _, _, link, category, title, author = post

    # 채널 아이디 리스트 가져오기
    channel_id_list = channelDataDB().get_on_channel(table_name)
    # 채널 아이디 리스트가 존재한다면
    if channel_id_list != None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed=discord.Embed(title=title, description=f"", color=color_code)
                embed.add_field(name="카테고리", value=category, inline=True)
                embed.add_field(name="글쓴이", value=author, inline=True)
                embed.add_field(name="링크", value=link, inline=False)
                # 미리보기 텍스트가 있을 경우
                if preview:
                    embed.add_field(name="미리보기", value=preview, inline=False)
                # 이미지 미리보기가 있을 경우
                if img_preview:
                    embed.set_image(url=img_preview)

                embed.set_footer(text=BOT_NAME_TAG_VER)
                await target_channel.send(embed=embed)

            except Exception as e:
                LOGGER.error(traceback.format_exc())