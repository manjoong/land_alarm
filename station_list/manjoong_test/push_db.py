import pymysql
def push_sale(name, price, img_link, naver_link, type, station, create_dt):
    push_sale = pymysql.connect(
        user='dev_user', 
        passwd='1q2w3e!@#',
        port=3306,
        host='3.34.189.107', 
        db='app_db', 
        charset='utf8'
    )

    cursor = push_sale.cursor(pymysql.cursors.DictCursor)

    sql = "SHOW FULL COLUMNS FROM `sale`;"
    cursor.execute(sql)
    result = cursor.fetchall()

    print(result)

push_sale()