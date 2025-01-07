import mysql.connector
from mysql.connector import Error

# MySQL数据库连接配置
config = {
    'user': 'root',  # 替换为你的MySQL用户名
    'password': 'mysql123',  # 替换为你的MySQL密码
    'host': '127.0.0.1',  # 或者你的MySQL服务器地址
    'port': '3306',  # 默认MySQL端口是3306
    'database': 'ai_data',
}
# 建立连接
connection = mysql.connector.connect(**config)
# 创建游标对象
cursor = connection.cursor()
# SQL查询语句，获取thumbnails表的前10行
query = "SELECT * FROM thumbnails LIMIT 10"

# 构建获取最后10行的SQL查询
# query = "SELECT * FROM thumbnails ORDER BY id DESC LIMIT 10;"
try:
    # 执行查询
    cursor.execute(query)
    # 获取查询结果
    results = cursor.fetchall()
    # 获取列名
    column_names = [desc[0] for desc in cursor.description]
    # 打印列名
    print(column_names)
    # 打印查询结果
    for row in results:
        print(row)
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # 关闭游标和连接
    cursor.close()
    connection.close()
