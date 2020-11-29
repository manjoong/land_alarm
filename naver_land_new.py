# -*- coding: utf-8 -*-

import threading
import time
import datetime
import requests
import json
import logging

URL = "https://m.land.naver.com/cluster/ajax/articleList"
old_id  #전에 돌렸을때 가장 최신이였던 매물의 id값

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

    # 'page': '1'
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



def check_jungja(page):
    global data  #매물 목록이 저장 될 변수
    global now #현재 시간
    data=[]

    param['page'] = page

    now= time.localtime()
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
    
    print(newPrdId, newPrdName)
    print(newPrdName)
    print(newPrdDate)
    print "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+9, now.tm_min, now.tm_sec)




def add_newst():
    global last #id가 있음을 확인하고 main의 while을 멈추는 트리거

    for idx, value in enumerate(data['body']):
        if value['atclNo'] != old_id:
            newest.append(data['body'][idx])
            print("we add ", value['atclNo'], "  ", idx)
        else:
            print("we found ", value['atclNo'], "  !!!!", idx)
            last = True
            break


            

def main():
    global newest #새로운 아이템 저장되는 배열
    global new_id #이번에 새로운 최신 매물 id 의 값
    global last #id가 있음을 확인하고 main의 while을 멈추는 트리거
    last = False

    newest = []
    page = 1
    while 1:
        check_jungja(page)
        if page == 1:
            new_id = data['body'][0]['atclNo'] #가장 최신인 매물의 id값 일단 저장
            # old_id = '2065012896'

        add_newst()
        
        if data['more'] == False: #끝까지 왔다면
            break
        else:
            page = page + 1
        
        if last == True: #해당되는 id 값을 찾았어도
            break

    print(len(newest))

    MyFile = open('new_prd_list_new.txt', 'a')
    MyFile.write("\n")
    MyFile.write(str(newest))
    MyFile.close()

    newest=[]
    print("new id: ", new_id, "old_id: ", old_id)
    old_id = new_id
    threading.Timer(300, main).start()

 
        

check_jungja(1) #최조 첫번째 매물을 알기위해 함수 실행
old_id=data['body'][0]['atclNo']

main()