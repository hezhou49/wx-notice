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
# 2个列表，分别存放学院和教务处的10条消息
links_school = []
links_teach = []
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
        target = soup.find_all("table", class_="ArtList")[:10]
    except:
        print("爬取失败,断网了，朋友")
        mail("报错", "爬虫断网了")
        return
    for eachOne in target[:7]:
        each_text = eachOne.tr.td.a.text
        each_href = eachOne.tr.td.a.get("href")
        # print(each_href, each_text)
        if each_href in links_school:
            pass
        else:
            print('进了')
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
    links_school.clear()
    for index, eachOne in enumerate(target):
        index = index + 1
        each_text = eachOne.tr.td.a.text
        each_href = eachOne.tr.td.a.get("href")
        links_school.append(each_href)
        # print(index, each_href, each_text)
        update_link_db("links_school", index, each_href, each_text)


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
        target = soup.find_all("a", class_="linkfont1")[:10]
    except:
        print("爬取失败,断网了，朋友")
        mail("报错", "爬虫断网了")
        return
    for eachOne in target[:7]:
        each_text = eachOne.text
        each_href = eachOne.get("href")
        # print(each_href, each_text)
        if each_href in links_teach:
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
    links_teach.clear()
    for index, eachOne in enumerate(target):
        index = index + 1
        each_text = eachOne.text
        each_href = eachOne.get("href")
        links_teach.append(each_href)
        # print(index, each_href, each_text)
        update_link_db("links_teach", index, each_href, each_text)


def insert_to_db(list_name, friend_name):
    # 打开数据库连接
    db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306, charset="utf8")

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


def update_link_db(list_name, number, each_link, each_text):
    # 打开数据库连接
    db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306)

    # 使用cursor()方法获取操作游标

    cur = db.cursor()

    sql_update_link = "update %s set link = '%s' where id = '%d'"
    sql_update_title = "update %s set title = '%s' where id = '%d'"

    try:
        cur.execute(sql_update_link % (list_name, each_link, number))  # 像sql语句传递参数
        # 提交
        db.commit()
        cur.execute(sql_update_title % (list_name, each_text, number))  # 像sql语句传递参数
        # 提交
        db.commit()
    except Exception as e:
        raise e
    finally:
        db.close()


def td(name):
    # 打开数据库连接
    db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306, charset="utf8")

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


def get_link_list():
    links_school.clear()
    links_teach.clear()
    # 打开数据库连接
    db = pymysql.connect(host='129.204.78.13', user="root", password="123", db="spider", port=3306, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql_school = "select * from links_school"
    sql_teach = "select * from links_teach"
    try:
        cur.execute(sql_school)  # 执行sql语句
        results_school = cur.fetchall()  # 获取查询的所有记录
        for row in results_school:
            links_school.append(row[1])
        cur.execute(sql_teach)  # 执行sql语句
        results_teach = cur.fetchall()  # 获取查询的所有记录
        for row in results_teach:
            links_teach.append(row[1])
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


def get_friend_list():
    friends_school.clear()
    friends_teaching.clear()
    # 打开数据库连接
    db = pymysql.connect(host='129.204.78.13', user="root", password="123", db="spider", port=3306, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql_school = "select * from friends_school"
    sql_teach = "select * from friends_teach"
    try:
        cur.execute(sql_school)  # 执行sql语句
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
    new_friend.send('自动处理：哈哈，我接受了你的好友请求')


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
        get_friend_list()
    if '2' == msg.text:
        status = insert_to_db('friends_teach', msg.sender.name)
        if status == 1:
            msg.reply_msg("您已经成功订阅教务处通告，无需再次操作")
        else:
            msg.reply_msg("成功订阅教务处通告")
        get_friend_list()
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
        get_friend_list()
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
        get_friend_list()


get_friend_list()
print("学院名单：")
print(friends_school)
print("教务处名单：")
print(friends_teaching)
get_link_list()
print("学院前十：")
print(links_school)
print("教务处前十：")
print(links_teach)
while 1:
    get_school()
    get_teaching()
    time.sleep(5)
    # print(links_school)
    # print(links_teach)
