# -*- coding: utf-8 -*-
import threading
import time
import requests
import json
import logging
import sys
from fake_useragent import UserAgent
import push_db
import delete_db
import send_alarm
from datetime import datetime
# from django.utils import timezone
from pytz import common_timezones, timezone



ua = UserAgent()

def check_connection_permit(que_file):
    f = open(str(que_file),'r')
    line = f.readlines()
    f.close()
    if len(line) != 0:
        last_line = line[-1]
        if last_line[-1] == '\n':
            last_line = last_line[:-1]
        if str(last_line) == str(str(sys.argv[1])+"_"+str(sys.argv[2])):
            return True

def request_connection_permit(que_file):
    f = open(str(que_file),'r+')
    lines = f.read()
    f.seek(0, 0) #get to the first position
    f.write(str(sys.argv[1]+"_"+str(sys.argv[2]).rstrip('\r\n') + '\n' + lines))
    f.close()


def delete_connection_permit(que_file):
    f = open(str(que_file),'r')
    lines = f.read()
    f.close()
    m=lines.split("\n")
    if m[-1] == '':
        m.pop()
    s="\n".join(m[:-1])
    f = open(str(que_file),'w+')
    for i in range(len(s)):
        f.write(s[i])
    f.close()

    

def find_station_location(station_id):
    print(station_id)
    location = []
    with open('/root/station.json') as json_file:
        station_data = json.load(json_file)
    station_result = station_data["subways"]["subway"]
    # print(station_result)
    for idx, value in enumerate(station_result):
        if int(value["stnId"]) == int(station_id):
            latitude = value["latitude"]
            longitude = value["longitude"]
            location.append(latitude)
            location.append(longitude)
            break
    return location
            
            


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
def get_prd(location):
    request_connection_permit("/root/que.txt") # que의 맨 위에 내 station id를 넣음
    time.sleep(3)
    if check_connection_permit("/root/que.txt")==None: #만약 내 차례가 오지 않았다면,
        while True:
            time.sleep(3) #3초 주기로 확인할 것
            print("대기")
            if check_connection_permit("/root/que.txt"): #만약 내 차례가 오면 나가기
                break  
    time.sleep(3)
    if check_connection_permit("/root/que.txt"):  # que를 통해 내 차례가 오면... naver api와 통신 실행
        URL = "https://m.land.naver.com/cluster/ajax/articleList"
        param = {
            'rletTpCd': str(sys.argv[2]),
            'tradTpCd': 'B1',
            'z': '15',
            'lat': str(location[0]),
            'lon': str(location[1]),
            'btm': str(location[0]-0.015),
            'lft': str(location[1]-0.015),
            'top': str(location[0]+0.015),
            'rgt': str(location[1]+0.015),
            'sort': 'dates',
        }

        # header = {
        #     'User-Agent': ua.random,
        #     #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
        # #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4280.67 Safari/537.36',
        #     # 'Referer': 'https://m.land.naver.com/'
        #     'Referer': 'https://www.kakao.com'
        # }

        logging.basicConfig(level=logging.INFO)

        page = 0
        result = []
        while True:
            page += 1
            param['page'] = page
            header_list = ["https://www.kakao.com", "https://www.naver.com", "https://www.hanmail.com", "https://www.google.com"]
            header = {
                'User-Agent': ua.random,
                #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
            #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4280.67 Safari/537.36',
                # 'Referer': 'https://m.land.naver.com/'
                'Referer': header_list[page%3]
            }

            data=[]
            resp = requests.get(URL, params=param, headers=header)
            time.sleep(10) #3초 쉬고 다음 역
            if resp.status_code != 200:
                logging.error('invalid status: %d' % resp.status_code)
            else:
                print("200 정상")

        
            # data= json_load_custom(resp.text)

            try:
                data = json.loads(resp.text)
                # data= json_load_custom(resp.text)
            except:
                print("제이슨 로드중 오류발생")
                print(resp.text)
                print(param)
                print(URL)
                print(header)

            for i in data['body']:
                result.append(i)

            if result is None:
                logging.error('no datas')

            if data['more'] == False: #끝까지 왔다면
                break

        delete_connection_permit(("/root/que.txt")) #실행이 끝났으니 맨 밑 실행 목록에서 지움
        return result

        
# def json_load_custom(text):
#     try:
#         data = json.loads(text)
#     except:
#         print("제이슨 로드중 오류발생")
#         print(text)
#     return data
            

def main():
    global old_prd_list
    global old_prd_id_list
    global station_location

    new_prd_id = [] #새로 추가된 매물의 id 배열
    delete_prd_id = [] # 삭제된 매물의 id 배열
    new_prd = [] #새로 추가된 매물의 전체 정보
    delete_prd = []  # 삭제된 매물의 전체 정보
    
    new_prd_list = get_prd(station_location) #새로 데이터 불러옴
    new_prd_id_list = make_id_list(new_prd_list) 
    new_prd_id = find_new_prd(old_prd_id_list, new_prd_id_list)
    delete_prd_id = find_delete_prd(old_prd_id_list, new_prd_id_list)
    
    for i in new_prd_id: #id 값을 기반으로 정보를 찾아 new_prd 배열에 넣음
        new_prd.append(find_content(i, new_prd_list))

    for i in delete_prd_id: #id 값을 기반으로 정보를 찾아 new_prd 배열에 넣음
        delete_prd.append(find_content(i, old_prd_list))

    KST = datetime.now(timezone('Asia/Seoul'))
    kst_datetime=KST.strftime('%Y-%m-%d %H:%M:%S')
    print(kst_datetime)
    print("기존 매물의 갯수는")
    print(len(old_prd_list))
    print("새 데이터의 매물의 갯수는")
    print(len(new_prd_list))
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

    if len(new_prd_list)!=0:
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
        MyFile = open('new_prd_list.txt', 'a')
        MyFile.write("\n")
        MyFile.write(kst_datetime)
        MyFile.write("추가된 매물")
        MyFile.write(str(new_prd))
        MyFile.write("삭제된 매물")
        MyFile.write(str(delete_prd))
        MyFile.close()
    
    if len(new_prd) != 0:
        for value in new_prd:
            sale_id=value['atclNo']
            sale_name=value['atclNm']
            sale_price=value['prc']
            if value.get('repImgUrl'):
                sale_img_url=value['repImgUrl']
            else:
                sale_img_url=""
            sale_naver_link = str("https://m.land.naver.com/article/info/" + value['atclNo'])
            sale_type = str(sys.argv[2])
            sale_station= str(sys.argv[1])
            sale_name=sale_name.encode('utf8')
            push_db.push_sale(sale_id, sale_name, sale_price, sale_img_url, sale_naver_link, sale_type, sale_station)
            send_alarm.send_sale_alarm(sale_station, sale_type, sale_name, sale_price, sale_naver_link)
        

    if len(delete_prd) != 0:
        for value in delete_prd:
            sale_id=value['atclNo']
            delete_db.delete_sale(sale_id)


    
    old_prd_list = new_prd_list #기존에 최신이였던 배열이 old로 갱신
    old_prd_id_list = new_prd_id_list 
    threading.Timer(10, main).start()



station_location=find_station_location(sys.argv[1])


old_prd_list = [] #기존에 불러온 매물 목록이 들어있는 배열
old_prd_id_list = [] # 기존에 불러온 매물 목록의 id만 모아둔 배열
old_prd_list = get_prd(station_location) #최초 한번 매물 리스트 함수 실행
old_prd_id_list = make_id_list(old_prd_list) #뽑은 매물 리스트에서 id값만 추출한 배열 생성

main()
# print(check_connection_permit("/root/que.txt"))
# request_connection_permit("/root/que.txt")
# delete_connection_permit("/root/que.txt")
