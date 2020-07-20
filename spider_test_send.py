# -*- coding: utf-8 -*-
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


def get_list():
    # 打开数据库连接
    db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306)

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
            if row[1] in friends_school:
                pass
            else:
                friends_school.append(row[1])
        cur.execute(sql_teach)  # 执行sql语句
        results_teach = cur.fetchall()  # 获取查询的所有记录
        for row in results_teach:
            if row[1] in friends_teaching:
                pass
            else:
                friends_teaching.append(row[1])
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


# dong = bot.friends().search('董师傅')[0]
# dong.send("抱歉打扰，这是一条机器人消息：\n\n由于代码优化，整体重启，推送此消息目的是确保先前订阅用户能正常收到消息\n如果你看到此消息，则说明操作成功，请忽略此消息\n抱歉打扰")
get_list()
print(friends_school)
# for eachFriend in friends_school:
#     object_friend = bot.friends().search(eachFriend)[0]
#     object_friend.send("群发机器消息，抱歉打扰：\n\n如下5条新消息，应该是今天发的，但消息日期填的是上周五22号，可能是上周忘了发吧。脚本设定只爬日期是当天的，所以没爬到，晚上再优化一下:"
#                        "\n“2018-2019学年和宗焊接助学金管理章程”"
#                        "\n“2018-2019学年和宗焊接奖学金评奖章程（本科生）”"
#                        "\n“上海庚奇奖学金评奖章程”"
#                        "\n“东洋电装奖学金”章程 "
#                        "\n“东洋电装助学金管理章程”")
#     object_friend.send("链接：http://www.auto.shu.edu.cn/synr/tzgg.htm")
#     print(object_friend.name)


# 发给自己
# object_friend = bot.friends().search('XX小舟')[0]
# object_friend.send("群发机器消息，抱歉打扰：\n\n如下5条新消息，应该是今天发的，但消息日期填的是上周五22号，可能是上周忘了发吧。脚本设定只爬日期是当天的，所以没爬到，晚上再优化一下:"
#                    "\n“2018-2019学年和宗焊接助学金管理章程”"
#                    "\n“2018-2019学年和宗焊接奖学金评奖章程（本科生）”"
#                    "\n“上海庚奇奖学金评奖章程”"
#                    "\n“东洋电装奖学金”章程 "
#                    "\n“东洋电装助学金管理章程”")
# object_friend.send("链接：http://www.auto.shu.edu.cn/synr/tzgg.htm")

