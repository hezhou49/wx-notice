#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time
from wxpy import *
from bs4 import BeautifulSoup
# 邮箱
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import pymysql

# 初始化机器人，扫码登陆
bot = Bot()
bot.enable_puid('wxpy_puid.pkl')
# 3个列表，分别存放需要发送信息的friends
friends_school = ['岳岳', '俞雯婕', '李新东', '魏煜杰', '17-机自-左净霭', '18级张鑫鹏', '傻鱼', '董师傅']
friends_teaching = ['岳岳', '俞雯婕', '李新东', '魏煜杰', '17-机自-左净霭', '18级张鑫鹏', '福建', '傻鱼', '芮易成', '董师傅']
# 例外列表，链接发送成功后加入，防止多次发送
exception = []
# 存放今日日期
today = ''
# 邮箱密码
my_sender = '1397095256@qq.com'  # 发件人邮箱账号
my_pass = 'ihxvjqjabwcqijcg'  # 发件人邮箱密码(当时申请smtp给的口令)
my_user = '1397095256@qq.com'  # 收件人邮箱账号，我这边发送给自己


def mail(topic, text):
    ret = True
    try:
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = formataddr(["何舟", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人昵称", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = topic  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def get_school():
    url = 'http://www.auto.shu.edu.cn/synr/tzgg.htm'
    # 模拟浏览器发送HTTP请求
    header = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
    except:
        print("爬取失败,断网了，朋友")
        mail("报错", "爬虫断网了")
        return
    target = soup.find_all("span", string=today)
    for eachOne in target:
        each_text = eachOne.parent.parent.td.a.text
        each_href = eachOne.parent.parent.td.a.get("href")
        if each_href in exception:
            pass
        else:
            # 发送链接、消息给好友
            real_href = "http://www.auto.shu.edu.cn/" + each_href[3:]
            print(real_href)
            print(each_text)
            mail("学院有新通知", "标题：" + each_text + "\n链接：" + real_href)
            for eachFriend in friends_school:
                object_friend = bot.friends().search(eachFriend)[0]
                object_friend.send("学院有新通知,标题：“" + each_text + "”")
                object_friend.send("链接：" + real_href)
            exception.append(each_href)


def get_teaching():
    url = 'http://www.jwc.shu.edu.cn/nry.jsp?urltype=tree.TreeTempUrl&wbtreeid=1015'
    # 模拟浏览器发送HTTP请求
    header = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
    except:
        print("爬取失败,断网了，朋友")
        mail("报错", "爬虫断网了")
        return
    target = soup.find_all("span", string=today)
    for eachOne in target:
        each_text = eachOne.parent.parent.td.a.text
        each_href = eachOne.parent.parent.td.a.get("href")
        if each_href in exception:
            pass
        else:
            # 发送链接、消息给好友
            real_href = "http://www.jwc.shu.edu.cn/" + each_href
            print(real_href)
            print(each_text)
            mail("教务处有新通知", "标题：" + each_text + "\n链接：" + real_href)
            for eachFriend in friends_teaching:
                object_friend = bot.friends().search(eachFriend)[0]
                object_friend.send("教务处有新通知,标题：“" + each_text + "”")
                object_friend.send("链接：" + real_href)
            exception.append(each_href)


while 1:
    timeGet = time.strftime('%Y-%m-%d', time.localtime())
    if timeGet == today:
        pass
    else:
        today = timeGet
        exception = []
    # print(today)
    # 学院通告
    get_school()
    # 教务处通告
    get_teaching()
    # get_graduate()
    print("##########################")
    print("已爬取名单：")
    print(exception)
    print("学院名单：")
    print(friends_school)
    print("教务处名单：")
    print(friends_teaching)
    time.sleep(5)

# ['岳岳', '俞雯婕', '李新东', '魏煜杰', '17-机自-左净霭', '18级张鑫鹏', '傻鱼', '董师傅']
# ['岳岳', '俞雯婕', '李新东', '魏煜杰', '17-机自-左净霭', '18级张鑫鹏', '福建', '傻鱼', '芮易成', '董师傅']
