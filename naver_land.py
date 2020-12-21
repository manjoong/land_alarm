# -*- coding: utf-8 -*-

import threading
import time
# import datetime
import requests
import json
import logging
from fake_useragent import UserAgent
from datetime import datetime
# from django.utils import timezone
from pytz import common_timezones, timezone
# from time import localtime, strftime




ua = UserAgent()
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
    'User-Agent': ua.random,
    'Referer': 'https://www.naver.com'
}

logging.basicConfig(level=logging.INFO)
page = 0

def delete_connection_permit(que_file):
    f = open(str(que_file),'r')
    lines = f.read()
    f.close()
    m=lines.split("\n")
    if m[-1] == '':
        print("공백이 있네..")
    print(m)
    # s="\n".join(m[:-1])
    # f = open(str(que_file),'w+')
    # for i in range(len(s)):
    #     f.write(s[i])
    # f.close()

def check_jungja():

    # now = time.localtime()


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
    
    KST = datetime.now(timezone('Asia/Seoul'))
    kst_datetime=KST.strftime('%Y-%m-%d %H:%M:%S')
    print(kst_datetime)
    print(newPrdId)
    print(newPrdName)
    print(newPrdDate)

    MyFile = open('new_prd_list.txt', 'a')
    MyFile.write("\n")
    MyFile.write(newPrdId)
    MyFile.write(newPrdName)
    MyFile.write(newPrdDate)
    MyFile.write(kst_datetime)
    MyFile.close()

    old_id = newPrdId
    #threading.Timer(900, check_jungja).start()

check_jungja()
# delete_connection_permit("/root/que.txt")
