# Kumon SE Board alarm

이 봇은 SE Board 매번 확인이 귀찮아서 만든 금오공대 컴퓨터소프트웨어공학과 학생들의 편의를 위해 만들어진 디스코드봇이다.

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
sample_config.py를 참고 하여 만들면 된다.
3. `python3 -m bot` 명령어로 실행한다.