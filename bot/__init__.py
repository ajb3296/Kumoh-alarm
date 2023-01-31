import os
import sys
import logging
from enum import Enum

# Bot version
BOT_VER = "V.1.0"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("3.6 버전 이상의 Python 이 있어야 합니다. 여러 기능이 해당 Python3.6 버전을 따릅니다. 봇 종료.")
    quit(1)

from bot.config import Development as Config

TOKEN             = Config.TOKEN
OWNERS            = Config.OWNERS
DebugServer       = Config.DebugServer
BOT_NAME          = Config.BOT_NAME
BOT_TAG           = Config.BOT_TAG
BOT_ID            = Config.BOT_ID
color_code        = Config.color_code
db_path           = Config.db_path
channel_db_path   = Config.channel_db_path

se_board_link     = Config.se_board_link
kumoh_square_link = Config.kumoh_square_link

EXTENSIONS = []
for file in os.listdir("bot/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))

BOT_NAME_TAG_VER = f"{BOT_NAME}{BOT_TAG} | {BOT_VER}"

class KumohSquarePage(Enum):
    Academic_Information = "sub06_01_01_01.do"
    Event_Information = "sub06_01_01_02.do"
    General_News = "sub06_01_01_03.do"

    @staticmethod
    def name_list():
        """ 이름 리스트 반환 """
        return list(map(lambda c: c.name, KumohSquarePage))

    @staticmethod
    def value_list():
        """ 값 리스트 반환 """
        return list(map(lambda c: c.value, KumohSquarePage))