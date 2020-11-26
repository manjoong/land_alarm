# -*- coding: utf-8 -*-

import threading
import time
import datetime
import requests
import json
import logging

URL = "https://m.land.naver.com/cluster/ajax/articleList"

# https://m.land.naver.com/cluster/ajax/articleList?rletTpCd=OPST&tradTpCd=B1&z=15&lat=37.366047&lon=127.108101&btm=37.3513279&lft=127.0858494&top=37.3807632&rgt=127.1303526&sort=dates&page=1

param = {
    'rletTpCd': 'OPST',
    'tradTpCd': 'B1',
    'z': '15',
    'lat': '37.366047',
    'lon': '127.108101',
    'btm': '37.3513279',
    'lft': '127.0858494',
    'top': '37.3807632',
    'rgt': '127.1303526',
    'sort': 'dates',
    'page': '1'

    # 'hscpNo': '19672',
    # 'tradTpCd': 'A1',
    # 'order': 'date_',
    # 'showR0': 'N',
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}

logging.basicConfig(level=logging.INFO)
page = 0

def check_jungja():

    now = time.localtime()


    resp = requests.get(URL, params=param, headers=header)
    if resp.status_code != 200:
        logging.error('invalid status: %d' % resp.status_code)

    data = json.loads(resp.text)

    result = data['body']

    newPrdId=result[0]['atclNo']
    newPrdName=result[0]['atclNm']
    newPrdDate=result[0]['atclCfmYmd']
    newPrdName=newPrdName.encode('utf8')
    newPrdDate=newPrdDate.encode('utf8')


    if result is None:
        logging.error('no datas')
    
    print(newPrdId)
    print(newPrdName)
    print(newPrdDate)
    print "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+9, now.tm_min, now.tm_sec)

    MyFile = open('new_prd_list.txt', 'a')
    MyFile.write("\n")
    MyFile.write(newPrdId)
    MyFile.write(newPrdName)
    MyFile.write(newPrdDate)
    MyFile.write("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+9, now.tm_min, now.tm_sec))
    MyFile.close()

    old_id = newPrdId

    threading.Timer(120, check_jungja).start()

check_jungja()
