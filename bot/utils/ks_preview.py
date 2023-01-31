from bs4 import BeautifulSoup

from bot.utils.crawler import getText

async def get_ks_preview(link: str) -> tuple:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    html = await getText(link, header)

    parse = BeautifulSoup(html, 'lxml')

    post = parse.find("div", {"class": "board-contents"})

    img_preview = None
    result = None

    if post is not None:
        # 텍스트 프리뷰
        post_text = post.find_all("p")
        text = ''
        for i in post_text:
            text += i.get_text() + " "
        
        if len(text) <= 100:
            result = text
        else:
            result = f'{text[:100]} ...[더보기]({link})'

        # 이미지 프리뷰
        try:
            img_preview = post.find('img')['src']
            if img_preview[0:4] != "http": # 링크가 아니라면
                img_preview = f'https://kumoh.ac.kr{img_preview}'
        except:
            pass
    
    return img_preview, result