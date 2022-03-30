#!/usr/bin/env python3.6
# !—*— coding:utf-8 —*—
# ！@Time   ：2022/3/29 10:29 下午
# ！@Author ：ferry_xie
# ！@Email  ：1359453864@qq.com
# ！@File   ：spider_detail.py

import time
import requests
from bs4 import BeautifulSoup
import sql_conn


# 网站请求
def response_get(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    html = requests.get(url=url, headers=headers)
    return html.text


# 从本地数据库抓取url
def get_visit_url_list(cols, table_name):
    str = ','
    cols = str.join(cols)

    connection = sql_conn.conn_sql()
    sql_cmd = 'select ' + cols + '  from ' + table_name
    result = sql_conn.read_sql(connection, sql_cmd)
    return result


def get_detail_url(table_name):  # 获得数据库中detail表里已有数据，并返回list
    connection = sql_conn.conn_sql()
    sql_cmd = 'select PaperUrl from ' + table_name  # 读取detail表
    detail_url_list = sql_conn.read_sql(connection, sql_cmd)
    result_list = []
    for record in detail_url_list:
        result_list.append(record[0])
    return result_list


def spider_paper():
    start = time.clock()  # 开始计时，统计总共花的时间

    Aimist = ['PaperName', 'Author', 'PaperUrl']
    AimTable = 'url_title'
    lines = get_visit_url_list(Aimist, AimTable)
    detail_url_list = get_detail_url('detail_info')
    # print(detail_url_list[1:10])
    process = 0  # 统计第多少次循环。方便显示运行进度

    for line in lines:
        process += 1
        print("当前进度：{}%".format(process / len(lines) * 100))
        try:
            paper_url = line[2]  # 每个tuple的第三个存储url
            if paper_url in detail_url_list:
                print("跳过")
                continue
            print(line[0])
            detail_url_list.append(paper_url)
            html = response_get("https:" + paper_url)
            soup = BeautifulSoup(html, 'html.parser')

            # 关键词
            keywords = soup.find('meta', attrs={'name': 'keywords'})['content']
            keywords_text = ';'.join(keywords.split())

            # 摘要
            abstract = soup.find('div', attrs={'class': 'xx_font'})
            abstract_text_1 = abstract.text.replace('"', "")
            abstract_text = abstract_text_1.replace('\n', "")

            # 期刊名称、出版日期
            title = soup.find('title').text
            t0 = title.split('《')
            t1 = t0[1].split('》')
            tt = t0[:1] + t1
            Journal_text = tt[1]
            date_text = tt[2].split('年')[0]

            # 存入数据库
            data = dict(PaperName=line[0], PaperUrl=line[2], Author=line[1], Abstracts=abstract_text,
                        Keywords=keywords_text, Journal=Journal_text, Year=date_text)
            sql_conn.store_to_detial('detail_info', data)

        except Exception as e:
            print('Error: ', e)

    end = time.clock()
    print('Running time: %s Seconds' % (end - start))


if __name__ == '__main__':
    spider_paper()
