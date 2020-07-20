import requests
from bs4 import BeautifulSoup
import pymysql


def update(title, number):
    # 打开数据库连接
    db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306)

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    cur = db.cursor()

    sql_update = "update title_school set title = '%s' where id = '%d'"

    try:
        cur.execute(sql_update % (title, number))  # 像sql语句传递参数
        # 提交
        db.commit()
    except Exception as e:
        # 错误回滚
        db.rollback()
    finally:
        db.close()


def insert(number, link, title):
    # 打开数据库连接
    db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306)

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    cur = db.cursor()
    sql_insert = "insert into links_teach(id,link,title) values('%d','%s','%s')"

    try:
        cur.execute(sql_insert % (number, link, title))
        # 提交，这句执行才能在数据库内看到记录
        db.commit()
    except Exception as e:
        # 错误回滚
        db.rollback()
    finally:
        db.close()


def get_list():
    # 打开数据库连接
    db = pymysql.connect(host='129.204.78.13', user="root", password="123", db="spider", port=3306, charset="utf8")

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql_select = "select * from link_school"

    try:
        cur.execute(sql_select)  # 执行sql语句
        results_school = cur.fetchall()  # 获取查询的所有记录
        for row in results_school:
            list_link_school.append(row[1])
        print(list_link_school)
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


list_link_school = []
list_link_teach = []
# get_list()
url = 'http://www.jwc.shu.edu.cn/nry.jsp?urltype=tree.TreeTempUrl&wbtreeid=1015'
# 模拟浏览器发送HTTP请求
header = {'User-Agent': 'Mozilla/5.0'}
try:
    response = requests.get(url, headers=header)
    response.raise_for_status()
    # 设置编码
    response.encoding = response.apparent_encoding
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # target = soup.find_all("span", string="2019-11-22")
    target = soup.find_all("a", class_="linkfont1")[:10]
    print(len(target))
    # target为列表
    for index, eachOne in enumerate(target):
        index = index + 1
        each_text = eachOne.text
        each_href = eachOne.get("href")
        if each_href in list_link_school:
            pass
        else:
            list_link_school.insert(index - 1, each_text)
            list_link_school.pop()
            print(list_link_school)
            # update(each_text, index)
            insert(index, each_href, each_text)

        print(index, each_href, each_text)


except:
    print("爬取失败")
