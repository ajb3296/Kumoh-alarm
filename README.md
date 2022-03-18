# Kumon SE Board alarm

이 봇은 SE Board 매번 확인이 귀찮아서 만든 금오공대 컴퓨터소프트웨어공학과 학생들의 편의를 위해 만들어진 디스코드봇이다.

## 봇 초대

https://discord.com/api/oauth2/authorize?client_id=950607518252556328&permissions=414464789568&scope=bot%20applications.commands

## How to install
1. bot 폴더 안에 config.py 파일을 만든다.
2. config.py 파일을 아래와 같이 작성한다.
```python
from bot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    DebugServer = [디버그 서버 id]
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_ID = 봇아이디
```
`sample_config.py`를 참고하여 만들면 된다.<br>
3. `python3 -m bot` 명령어로 실행한다.