# -*- coding: utf-8 -*-

# from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

url = 'https://m.land.naver.com/article/image/2068224408'

header = {
    'User-Agent': ua.random,
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
#'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4280.67 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}



html = requests.get(url,allow_redirects=False, headers=header)
# res = urlopen(req)
# html = res.read().decode('cp949')
# print(html.text)

bs = BeautifulSoup(html.text, 'html.parser')

print(bs)
tags = bs.findAll('div', attrs={'class': 'wrap wrap_photo_list'})

for tag in tags :
    # 검색된 태그에서 a 태그에서 텍스트를 가져옴
    print(tag.a.text)