# -*- coding: utf-8 -*-

import pymysql
def push_sale(sale_id, sale_name, sale_price, sale_img_link, sale_naver_link, sale_type, sale_station):
# def push_sale():
    conn = pymysql.connect(
        user='dev_user', 
        passwd='1q2w3e!@#',
        port=3306,
        host='3.34.189.107', 
        db='app_db', 
        charset='utf8'
    )


    try:
        # INSERT
        with conn.cursor() as curs:
            sql = "insert into sale(naver_id, name, price, img_link, naver_link, type, station) values (%s, %s, %s, %s, %s, %s, %s)"
            # curs.execute(sql, (str(name), price, str(), 'www.naver.com/183', 'OPST', '468'))
            curs.execute(sql, (sale_id, sale_name, sale_price, sale_img_link, sale_naver_link, sale_type, sale_station))
    
        conn.commit()
    
        # SELECT
        with conn.cursor() as curs:
            sql = "select * from sale where id=%s"
            curs.execute(sql, (str(sale_id)))
            rs = curs.fetchall()
            for row in rs:
                print(row)
    
    finally:
        conn.close()




    # # cursor = push_sale.cursor(pymysql.cursors.DictCursor)
    # curs = push_sale.cursor()
    # sql = """insert into sale(name, price, img_link, naver_link, type, station, create_dt) values (%s, %s, %s, %s, %s, %s, %s)"""

    # curs.execute(sql, ('파빌리온', 1.5, 'www.naver.com', 'www.naver.com/183', 'OPST', '468', '2020-12-24 17:22:21'))

    # # sql = "SHOW FULL COLUMNS FROM `sale`;"
    # curs.execute(sql)
    # result = curs.fetchall()

    # print(result)

push_sale("204502", "위브타워", "50000", "www.naver.com/image/23", "www.naver.com/land/204502", "OPST", "8")