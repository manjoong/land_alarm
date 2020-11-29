# -*- coding: utf-8 -*-
import threading
import time
import datetime
import requests
import json
import logging


# 새로운 매물 찾는 함수
def find_new_prd(old_id_list, new_id_list):
    new_prd_list=[]
    new_prd_list = list(set(new_id_list) - set(old_id_list))
    return new_prd_list

# 삭제된 매물 찾는 함수
def find_delete_prd(old_id_list, new_id_list):
    delete_prd_list=[]
    delete_prd_list = list(set(old_id_list) - set(new_id_list))
    return delete_prd_list

#모든 내용을 담고 있는 배열에서 id만 들어있는 배열을 만드는 함수
def make_id_list(all_content):
    id_list=[]
    for idx, value in enumerate(all_content):
        id_list.append(value['atclNo'])
    # print(id_list)
    return id_list

# id값을 기반으로 매물 정보를 찾는 함수
def find_content(id, all_content):
    for idx, value in enumerate(all_content):
        if value['atclNo'] == id:
            return all_content[idx]
            break
        


#외부에서 데이터를 불러오는 함수
def get_prd():
    URL = "https://m.land.naver.com/cluster/ajax/articleList"
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
    }

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }

    logging.basicConfig(level=logging.INFO)

    page = 0
    result = []
    while True:
        page += 1
        param['page'] = page
        data=[]
        resp = requests.get(URL, params=param, headers=header)
        if resp.status_code != 200:
            logging.error('invalid status: %d' % resp.status_code)

        data = json.loads(resp.text)

        for i in data['body']:
            result.append(i)

        if result is None:
            logging.error('no datas')

        if data['more'] == False: #끝까지 왔다면
            break

    # newPrdId=result[0]['atclNo']
    # newPrdName=result[0]['atclNm']
    # newPrdDate=result[0]['atclCfmYmd']
    # newPrdName=newPrdName.encode('utf8')
    # newPrdDate=newPrdDate.encode('utf8')
   
    # print(newPrdId, newPrdName)
    # print(newPrdName)
    # print(newPrdDate)
    # print "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+9, now.tm_min, now.tm_sec)
    # print(result)
    return result
            

def main():
    global old_prd_list
    global old_prd_id_list

    now= time.localtime()
    new_prd_id = [] #새로 추가된 매물의 id 배열
    delete_prd_id = [] # 삭제된 매물의 id 배열
    new_prd = [] #새로 추가된 매물의 전체 정보
    delete_prd = []  # 삭제된 매물의 전체 정보
    
    new_prd_list = get_prd() #새로 데이터 불러옴
    new_prd_id_list = make_id_list(new_prd_list) 
    new_prd_id = find_new_prd(old_prd_id_list, new_prd_id_list)
    delete_prd_id = find_delete_prd(old_prd_id_list, new_prd_id_list)
    
    for i in new_prd_id: #id 값을 기반으로 정보를 찾아 new_prd 배열에 넣음
        new_prd.append(find_content(i, new_prd_list))

    for i in delete_prd_id: #id 값을 기반으로 정보를 찾아 new_prd 배열에 넣음
        delete_prd.append(find_content(i, old_prd_list))

    print "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+9, now.tm_min, now.tm_sec)
    print("기존 매물의 갯수는")
    print(len(new_prd_list))
    print("새 데이터의 매물의 갯수는")
    print(len(old_prd_list))
    print("새로운 매물의 id는")
    if len(new_prd) != 0:
        for i in new_prd:
            print(i)
    else:
        print("새로운 매물이 없습니다.")

    print("삭제된 매물의 id는")
    if len(delete_prd) != 0:
        for i in delete_prd:
            print(i)
    else:
        print("삭제된 매물이 없습니다.")
    
    print("가장 최상의 매물은")
    newPrdId=new_prd_list[0]['atclNo']
    newPrdName=new_prd_list[0]['atclNm']
    newPrdDate=new_prd_list[0]['atclCfmYmd']
    newPrdName=newPrdName.encode('utf8')
    newPrdDate=newPrdDate.encode('utf8')
    print(newPrdName)
    print(newPrdDate)
    print(newPrdId)

    print("새로운 매물과 삭제된 매물은 5분씩 검색하며, 정보는 new_prd_list_new_2.txt에 저장 됩니다.")

    if len(new_prd) != 0 or len(delete_prd) !=0:
        MyFile = open('new_prd_list_new_2.txt', 'a')
        MyFile.write("\n")
        MyFile.write("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+9, now.tm_min, now.tm_sec))
        MyFile.write("추가된 매물")
        MyFile.write(str(new_prd))
        MyFile.write("삭제된 매물")
        MyFile.write(str(delete_prd))
        MyFile.close()


    
    old_prd_list = new_prd_list #기존에 최신이였던 배열이 old로 갱신
    old_prd_id_list = new_prd_id_list 
    threading.Timer(300, main).start()

 

# new_prd_list = [] #새로 불러온 매물 목록이 들어있는 배열
old_prd_list = [] #기존에 불러온 매물 목록이 들어있는 배열
# new_prd_id_list = [] # 새로 불러온 매물 목록의 id만 모아둔 배열
old_prd_id_list = [] # 기존에 불러온 매물 목록의 id만 모아둔 배열

old_prd_list = get_prd() #최초 한번 매물 리스트 함수 실행
old_prd_id_list = make_id_list(old_prd_list) #뽑은 매물 리스트에서 id값만 추출한 배열 생성

main()

