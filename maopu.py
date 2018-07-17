#coding:utf-8
from lxml import etree
import pymysql
from selenium import webdriver

#网页解析
#1.解析出主页标题和网址
browser = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe')
browser.get('http://dzh.mop.com/xiaohua.html')
html1 =etree.HTML(browser.page_source)
url_list=html1.xpath('//div[@class="dzh-today-list"]/ul/li/a/@href')
title_list=html1.xpath('//div[@class="dzh-today-list"]/ul/li/a/text()')

#2.解析出文章的具体信息
def detail(i):
    browser = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe')
    browser.get(url_list[i])
    html2 = etree.HTML(browser.page_source)
    post_date = html2.xpath('//div/span[@class="post-date"]/span/text()')
    post_click = html2.xpath('//div/span/span[@class="post-click"]/em/text()')
    post_reply = html2.xpath('//div/span/span[@class="post-reply"]/em/text()')
    c = [post_date[0], post_click[0], post_reply[0]]
    return c

#mysql写入
connection=pymysql.connect(host='localhost',user='root',passwd='1989425',db='fenxi',charset='utf8')
cursor=connection.cursor()
for j in range(len(url_list)):
    a=detail(j)
    sql='insert into python_work (title,url,p_date,p_click,p_reply) values (%s,%s,%s,%s,%s)'
    parm=(title_list[j],url_list[j],a[0],a[1],a[2])
    cursor.execute(sql,parm)
    print('数据获取成功')
    connection.commit()
    print('修改成功')
cursor.close()
connection.close()
