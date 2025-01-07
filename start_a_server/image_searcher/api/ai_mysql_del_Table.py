import mysql.connector

# 数据库连接参数
config = {
    'user': 'root',  # 替换为你的MySQL用户名
    'password': 'mysql123',  # 替换为你的MySQL密码
    'host': '127.0.0.1',  # 或者你的MySQL服务器地址
    'port': '3306',  # 默认MySQL端口是3306

    'database': 'ai_data',
    'raise_on_warnings': True
}

# 尝试连接数据库并执行查询
try:
    # 建立连接
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # SQL查询语句
    query = "SELECT COUNT(*) FROM thumbnails;"

    # 执行查询
    cursor.execute(query)

    # 获取查询结果
    count = cursor.fetchone()[0]
    print(f"Table 'thumbnails' has {count} rows.")

    # # 删除表的SQL命令
    # delete_table_query = "DROP TABLE IF EXISTS thumbnails"
    # # 执行SQL命令
    # cursor.execute(delete_table_query)
    # # 提交更改
    # connection.commit()
    # print("thumbnails 表已从数据库中删除。")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # 关闭游标和连接
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
