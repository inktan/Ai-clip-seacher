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

try:
    # 连接数据库
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()

        # 更新thumbnails表中的id列，每个id减1
        update_query = "UPDATE thumbnails SET id = id - 1"
        cursor.execute(update_query)

        # 提交更改
        connection.commit()

        # 获取受影响的行数
        affected_rows = cursor.rowcount
        print(f"Total rows affected: {affected_rows}")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # 关闭游标和连接
    if connection.is_connected():
        cursor.close()
        connection.close()
