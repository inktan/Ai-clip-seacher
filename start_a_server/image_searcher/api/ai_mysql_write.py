import sqlite3
import mysql.connector

# 连接到SQLite数据库
db_path = 'Y:/GOA-AIGC/98-goaTrainingData/Arch_200px_/stored_paths.db'
sqlite_conn = sqlite3.connect(db_path)
sqlite_cursor = sqlite_conn.cursor()
table_name_data_normal = 'data_normal'

# 从SQLite数据库中查询数据
sqlite_query = f"SELECT PATH, thumbnail_width, thumbnail_height FROM {table_name_data_normal}"  # 替换为你的表名
sqlite_cursor.execute(sqlite_query)
rows = sqlite_cursor.fetchall()

# MySQL数据库连接配置
mysql_config = {
    'user': 'root',  # 替换为你的MySQL用户名
    'password': 'mysql123',  # 替换为你的MySQL密码
    'host': '127.0.0.1',  # 或者你的MySQL服务器地址
    'port': '3306',  # 默认MySQL端口是3306
    'database': 'ai_data',
}

# 连接到My`SQL数据库
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# 创建MySQL表
create_table_query = """
CREATE TABLE IF NOT EXISTS thumbnails (
    PATH TEXT,
    thumbnail_width INT,
    thumbnail_height INT
)
"""
mysql_cursor.execute(create_table_query)

# 分批写入的大小
batch_size = 20000
insert_query = """
INSERT INTO thumbnails (PATH, thumbnail_width, thumbnail_height)
VALUES (%s, %s, %s)
"""
try:
    # 开始写入数据
    for i in range(0, len(rows), batch_size):
        # 每次取batch_size大小的数据
        batch = rows[i:i + batch_size]
        # 执行批量插入
        mysql_cursor.executemany(insert_query, batch)
        # 提交事务
        mysql_conn.commit()
        print(f"Committed batch starting at index {i}")

except mysql.connector.Error as e:
    print(f"Error: {e}")
    # 发生错误时回滚事务
    mysql_conn.rollback()

finally:
    # 关闭游标和连接
    if mysql_conn.is_connected():
        mysql_cursor.close()
        mysql_conn.close()
        print("MySQL connection is closed")

# 将数据写入MySQL数据库
insert_query = """
INSERT INTO thumbnails (PATH, thumbnail_width, thumbnail_height)
VALUES (%s, %s, %s)
"""
mysql_cursor.executemany(insert_query, rows)

# 提交更改并关闭连接
mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()

sqlite_cursor.close()
sqlite_conn.close()

print("数据已成功从SQLite迁移到MySQL")
