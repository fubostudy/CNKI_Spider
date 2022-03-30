#!/usr/bin/env python3.6
# !—*— coding:utf-8 —*—
# ！@Time   ：2022/3/29 10:29 下午
# ！@Author ：ferry_xie
# ！@Email  ：1359453864@qq.com
# ！@File   ：spider_detail.py

import pymysql

"""
需要在数据库中提前建立数据库和表
数据库：CNKI
表：url_title ; 字段：NUM、PaperName、PaperUrl、Author
表：detail_info ; 字段：NUM、PaperName、PaperUrl、Author、Year、Journal、Abstracts、Keywords
"""

# 在这里输入数据库的名称，需要提前建立
DataBase = 'CNKI'


# 连接数据库
def conn_sql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='11111111', db='CNKI', charset='utf8')
    return conn


# 存储文章具体信息的数据库接口，这里的tbname在spider_detail中调用传入
def store_to_detial(tbname, dt):
    try:
        conn = conn_sql()
        cursor = conn.cursor()
        ls = [(k, v) for k, v in dt.items() if k is not None]
        # sql语句
        sentence = 'INSERT INTO %s (' % tbname + ','.join([i[0] for i in ls]) + ') VALUES (\"' + '","'.join(
            [i[1] for i in ls]) + '\");'
        # print(sentence)
        cursor.execute(sentence)
        conn.commit()
        cursor.close()
    except Exception as e:
        print('Error: ', e)


# 存储文章url的数据库接口
def store_to_sql(dt, connect, cursor):
    print("1")
    tbname = 'url_title'
    ls = [(k, v) for k, v in dt.items() if k is not None]
    # sql语句
    sentence = 'INSERT INTO %s (' % tbname + ','.join([i[0] for i in ls]) + ') VALUES (\"' + '","'.join(
        [i[1] for i in ls]) + '\");'
    # print(sentence)
    cursor.execute(sentence)
    connect.commit()
    return ""


# 读取sql
def read_sql(conn, sentence):
    cursor = conn.cursor()
    cursor.execute(sentence)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result  # 返回为字典形式

# 测试
# if __name__ == '__main__':
#     conn = conn_sql()
#     cursor = conn.cursor()
#     sentence = ' '
#     cursor.execute(sentence)
#     connect.commit()
