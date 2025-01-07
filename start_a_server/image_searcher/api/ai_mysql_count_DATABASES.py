import mysql.connector

# 配置数据库连接参数
config = {
    'user': 'root',  # 替换为你的MySQL用户名
    'password': 'mysql123',  # 替换为你的MySQL密码
    'host': '127.0.0.1',  # 或者你的MySQL服务器地址
    'port': '3306',  # 默认MySQL端口是3306
}

# 建立数据库连接
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # 执行SQL查询来获取所有数据库名
    cursor.execute("SHOW DATABASES")

    # 获取查询结果
    databases = cursor.fetchall()

    # 打印数据库数量和名称
    print(f"Total databases: {len(databases)}")
    for (database,) in databases:
        print(database)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
