import os
import discord
import asyncio
import traceback

from bot.utils.database import *
from bot.utils.se_preview import get_preview
from bot import LOGGER, BOT_NAME_TAG_VER, se_board_link, db_path

async def broadcast(bot):
    """ SE게시판 새 글 알림 전송 """
    if not os.path.exists(db_path):
        await asyncio.sleep(5)
    while True:
        latest_data_id = seBoardDB().get_latest_data_id()
        # None 이 아닐 경우 반복문 탈출
        if latest_data_id is not None:
            break
        # None 일 경우 5초 대기
        await asyncio.sleep(5)
    await asyncio.sleep(5)
    
    while True:
        while True:
            now_latest_data_id = seBoardDB().get_latest_data_id()
            # None 이 아닐 경우 반복문 탈출
            if now_latest_data_id is not None:
                break
            # None 일 경우 5초 대기
            await asyncio.sleep(5)
        if latest_data_id != now_latest_data_id:
            for data_id in range(latest_data_id + 1, now_latest_data_id + 1):
                # get post
                post = seBoardDB().get_database_from_id(data_id)
                # 데이터베이스에 정보가 존재할 경우
                if post is not None:
                    try:
                        img_preview, preview = await get_preview(post[1])
                    except:
                        # 글 수정/삭제되었을 경우 오류 예외처리
                        img_preview = None
                        preview = None

                    # 메시지 전송
                    if post is not None:
                        LOGGER.info(f"Send msg : {post}")
                        await send_msg(bot, post, preview, img_preview)

            latest_data_id = now_latest_data_id
        await asyncio.sleep(60)

async def send_msg(bot, post: tuple, preview: (str | None), img_preview: (str | None)):
    """ 메시지 전송 """
    # 빨간색
    if post[3] in ["오득환", "김선명", "이현아", "김시관", "신윤식", "이해연", "김병만", "전태수", "학과장"]:
        color = 0xff0000
        important = ":red_circle: 매우 중요"
        everyone_ping = True
    # 오렌지색
    elif post[3] in ["이한나[조교]", "학생회"]:
        color = 0xff7f00
        important = ":orange_circle: 중요"
        everyone_ping = False
    # 초록색
    else:
        color = 0x008000
        important = ":green_circle: 보통"
        everyone_ping = False

    # 채널 아이디 리스트 가져오기
    channel_id_list = KumohSquarePage.name_list() + ["SE_Board"]
    # 채널 아이디 리스트가 존재한다면
    if channel_id_list != None:
        # 채널아이디별 메시지 전송
        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            # 메시지 전송에 실패할 경우를 대비해 3번 시도
            for _ in range(3):
                try:
                    # 중요도에 따라 everyone ping
                    if everyone_ping:
                        await target_channel.send("@everyone")
                    embed=discord.Embed(title=post[2], description=f"", color=color)
                    embed.add_field(name="글쓴이", value=post[3], inline=True)
                    embed.add_field(name="중요도", value=important, inline=True)
                    embed.add_field(name="링크", value=f"{se_board_link}freeboard/{post[1]}", inline=False)
                    # 미리보기 텍스트가 있을 경우
                    if preview:
                        embed.add_field(name="미리보기", value=preview, inline=False)
                    # 이미지 미리보기가 있을 경우
                    if img_preview:
                        embed.set_image(url=img_preview)

                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    await target_channel.send(embed=embed)

                    break
                except Exception as e:
                    LOGGER.error(traceback.format_exc())