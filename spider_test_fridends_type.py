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
friends_school = []
friends_teaching = []
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
                time.sleep(0.5)
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
                time.sleep(0.5)
            exception.append(each_href)


def insert_to_db(list_name, friend_name):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123", db="spider", port=3306, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql = "select * from %s where friendname='%s'"
    sql_insert = """insert into %s(friendname) values('%s')"""
    try:
        cur.execute(sql % (list_name, friend_name))  # 执行sql语句

        results = cur.fetchall()  # 获取查询的所有记录
        if len(results) == 0:
            print('没查到，即将添加')
            cur.execute(sql_insert % (list_name, friend_name))
            db.commit()
            return 0
        # 遍历结果
        else:
            print("已经在数据库内了")
            return 1
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


def td(name):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123", db="spider", port=3306, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql_teach = "select * from friends_teach where friendname='%s'"
    sql_school = "select * from friends_school where friendname='%s'"
    sql_delete_teach = "delete from friends_teach where friendname='%s'"
    sql_delete_school = "delete from friends_school where friendname='%s'"
    try:
        cur.execute(sql_teach % name)  # 执行sql语句
        results_teach = cur.fetchall()  # 获取查询的所有记录

        cur.execute(sql_school % name)  # 执行sql语句
        results_school = cur.fetchall()  # 获取查询的所有记录

        if len(results_teach) != 0 and len(results_school) != 0:
            cur.execute(sql_delete_teach % name)
            db.commit()
            cur.execute(sql_delete_school % name)
            db.commit()
            return 1
        elif len(results_school) != 0:
            cur.execute(sql_delete_school % name)
            db.commit()
            return 2
        elif len(results_teach) != 0:
            cur.execute(sql_delete_teach % name)
            db.commit()
            return 3
        else:
            return 4
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


def get_list():
    friends_school.clear()
    friends_teaching.clear()
    # 打开数据库连接
    db = pymysql.connect(host='localhost', user="root", password="123", db="spider", port=3306, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql_school = "select * from friends_school"
    sql_teach = "select * from friends_teach"
    try:
        cur.execute(sql_school) # 执行sql语句
        results_school = cur.fetchall()  # 获取查询的所有记录
        for row in results_school:
            friends_school.append(row[1])
        cur.execute(sql_teach)  # 执行sql语句
        results_teach = cur.fetchall()  # 获取查询的所有记录
        for row in results_teach:
            friends_teaching.append(row[1])
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


@bot.register(msg_types=FRIENDS)
# 自动接受验证信息的好友请求
def auto_accept_friends(msg):
    new_friend = bot.accept_friend(msg.card)
    # 或 new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求')


@bot.register(Friend, TEXT)
# 好友订阅通知
def service(msg):
    print('######')
    print(msg.sender.name + ':发来消息：')
    print(msg.text)
    print('######')
    if '通知' == msg.text:
        msg.reply_msg("你想订阅哪些网站通知？\n 请回复标题,如：1,2或12\n1.机自学院通告\n2.教务处通告\n注：订阅成功后可回复TD取消订阅")
    if '1' == msg.text:
        status = insert_to_db('friends_school', msg.sender.name)
        if status == 1:
            msg.reply_msg("您已经成功订阅机自学院通告，无需再次操作")
        else:
            msg.reply_msg("成功订阅机自学院通告")
        get_list()
    if '2' == msg.text:
        status = insert_to_db('friends_teach', msg.sender.name)
        if status == 1:
            msg.reply_msg("您已经成功订阅教务处通告，无需再次操作")
        else:
            msg.reply_msg("成功订阅教务处通告")
        get_list()
    if '12' == msg.text:
        status = insert_to_db('friends_school', msg.sender.name)
        if status == 1:
            msg.reply_msg("您已经成功订阅机自学院通告，无需再次操作")
        else:
            msg.reply_msg("成功订阅机自学院通告")
        status1 = insert_to_db('friends_teach', msg.sender.name)
        if status1 == 1:
            msg.reply_msg("您已经成功订阅教务处通告，无需再次操作")
        else:
            msg.reply_msg("成功订阅教务处通告")
        get_list()
    if "TD" == msg.text:
        status = td(msg.sender.name)
        if status == 1:
            msg.reply_msg("成功退订学院、教务处通告")
        elif status == 2:
            msg.reply_msg("成功退订机自学院通告")
        elif status == 3:
            msg.reply_msg("成功退订教务处通告")
        else:
            msg.reply_msg("您还未订阅")
        get_list()


get_list()
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
