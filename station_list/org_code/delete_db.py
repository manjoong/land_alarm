# -*- coding: utf-8 -*-

import pymysql
def delete_sale(sale_id):
# def delete_sale():
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
            sql = "delete from sale where naver_id=(%s)"
            curs.execute(sql, (sale_id))
            # curs.execute(sql, (20))
    
        conn.commit()
    
        # SELECT
        # with conn.cursor() as curs:
        #     sql = "select * FROM sale ORDER BY date create_dt DESC limit 1"
        #     curs.execute(sql)
        #     rs = curs.fetchall()
        #     for row in rs:
        #         print(row)
    
    finally:
        conn.close()

# delete_sale(2065547517)


