import pymysql

# 打开数据库连接
db = pymysql.connect(host="129.204.78.13", user="root", password="123", db="spider", port=3306)

# 使用cursor()方法获取操作游标
cur = db.cursor()

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名
sql = "select * from friends"
try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    print("id", "friend")
    # 遍历结果
    for row in results:
        id = row[0]
        friend = row[1]
        print(id, friend)
except Exception as e:
    raise e
finally:
    db.close()  # 关闭连接
