#!/usr/bin/env python3.6
# !—*— coding:utf-8 —*—
# ！@Time   ：2022/3/29 10:29 下午
# ！@Author ：ferry_xie
# ！@Email  ：1359453864@qq.com
# ！@File   ：spider_detail.py

import time
import requests
from lxml import etree
import sql_conn

page_url = 20  # 每页显示21篇论文

# 获得url返回信息
class POST:
    def __init__(
            # Content是编码后的检索关键词，需要自己网页F12看并在这里修改，这里是气候变化
            self, url='http://search.cnki.com.cn/Search/Result',
            param={'searchType': 'MulityTermsSearch', 'ParamIsNullOrEmpty': 'false',
                   'Islegal': 'false', 'Content': '气候变化', 'Order': '1', 'Page': '1'}):
        self.url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'
        }
        self.param = param

    def response(self):
        html = requests.post(url=self.url, data=self.param, headers=self.header)
        return html.text


# 使用xpath获取文章的url存入数据库
def get_paper_url(pages, post_form):
    conn = sql_conn.conn_sql()
    cursor = conn.cursor()

    for i in range(1, pages + 1):
        post_form['Page'] = str(i)
        try:
            emp2 = POST(param=post_form)  # 使用默认参数
            response = emp2.response()
            tree = etree.HTML(response)
        except:
            print("出错跳过")
            continue
        for num in range(1, page_url + 2):  # 每页有20个herf,,xpath从1起始
            try:
                url = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p/a/@href')[0])
                title = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p/a/@title')[0])
                author = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p[3]/span[1]/@title')[0])
                dt = {'PaperName': title, 'PaperUrl': url, 'Author': author}  # 字典
                print(dt)
                sql_conn.store_to_sql(dt, conn, cursor)  # 存入数据库命令,每条写入一次
            except:
                continue

        # 获取结束时间
        end = time.clock()
        print('获取文章详情页链接共用时：%s Seconds' % (end - start))


if __name__ == '__main__':
    # 获取开始时间
    start = time.clock()

    index_url = 'https://search.cnki.com.cn/Search/Result'
    page = '10000'  # 最大页数
    keyword = '气候变化'  # 检索的关键词
    form = {'searchType': 'MulityTermsSearch', 'ParamIsNullOrEmpty': 'false',
            'Islegal': 'false', 'Content': keyword, 'Order': '1', 'Page': page}
    emp1 = POST(index_url, form)  # 创建第一个类对象，用于获得返回数据
    html1 = emp1.response()

    maxpage = 10000  # 最大页数
    get_paper_url(maxpage, form)  # 获取各检索结果文章链接
