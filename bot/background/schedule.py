import json
import asyncio
import datetime
import traceback
from dateutil.relativedelta import relativedelta

from bot.utils.crawler import getText
from bot.utils.database import channelDataDB

async def schedule(bot):
    """ 금오공대 학사일정 디스코드 일정으로 등록 """
    # 스케쥴 가져오기
    schedules = await get_schedule()

    # 동기화 켜진 서버 목록 가져오기
    server_list = channelDataDB().get_on_channel("Schedule")

    while True:
        if datetime.datetime.now().hour == 0:
            if server_list is not None:
                # 각 서버별로
                for server_id in server_list:
                    # 스케쥴 등록
                    for schedule in schedules:
                        articleNo = str(schedule["articleNo"])
                        title = schedule["articleTitle"]
                        start_time = datetime.datetime.strptime(f"{schedule['etcChar6']} 0:0:0", '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=9)
                        end_time = datetime.datetime.strptime(f"{schedule['etcChar7']} 23:59:59", '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=9)

                        # 시작시간이 지금보다 미래라면
                        if start_time > datetime.datetime.now():
                            # 서버 가져오기
                            try:
                                get_server = bot.get_guild(server_id)
                            except:
                                print(traceback.format_exc())
                            else:
                                # 서버에 등록된 스케쥴 가져오기
                                schedules_in_server = get_server.scheduled_events

                                # description이 일치하는 스케쥴 찾기
                                server_data = None
                                for sc in schedules_in_server:
                                    if sc.description == articleNo:
                                        server_data = sc
                                        break

                                # 서버에 스케쥴이 등록되어 있지 않으면
                                if server_data is None:
                                    # 서버에 등록
                                    await get_server.create_scheduled_event(name=title,
                                                                    description=articleNo,
                                                                    location="금오공과대학교",
                                                                    start_time=start_time,
                                                                    end_time=end_time)
                                # 서버에 스케쥴이 등록되어 있으면
                                else:
                                    # 변경점 확인
                                    if server_data.name != title or server_data.start_time != start_time or server_data.end_time != end_time:
                                        # 다를경우 수정
                                        await server_data.edit(name=title,
                                                        description=articleNo,
                                                        location="금오공과대학교",
                                                        start_time=start_time,
                                                        end_time=end_time)
        await asyncio.sleep(3600)

async def get_schedule() -> list:
    """ 금오공대 학사일정 가져오기 """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    this_year_link = f"https://www.kumoh.ac.kr/app/common/selectDataList.do?sqlId=jw.Article.selectCalendarArticle&modelNm=list&jsonStr=%7B%22year%22%3A%22{datetime.datetime.now().year}%22%2C%22bachelorBoardNoList%22%3A%5B%2212%22%5D%7D"
    next_year_link = f"https://www.kumoh.ac.kr/app/common/selectDataList.do?sqlId=jw.Article.selectCalendarArticle&modelNm=list&jsonStr=%7B%22year%22%3A%22{(datetime.datetime.now() + relativedelta(years=1)).year}%22%2C%22bachelorBoardNoList%22%3A%5B%2212%22%5D%7D"

    this_year = await getText(this_year_link, header)
    this_year = json.loads(this_year)['list']

    next_year = await getText(next_year_link, header)
    next_year = json.loads(next_year)['list']

    return this_year + next_year