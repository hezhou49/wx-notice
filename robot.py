from wxpy import *

# 初始化机器人，扫码登陆
bot = Bot()
my_friend = bot.friends().search('XX小舟', sex=MALE)[0]
my_friend.send('Hello WeChat!')
