import mysql.connector

# 配置数据库连接参数
config = {
    'user': 'root',  # 替换为你的MySQL用户名
    'password': 'mysql123',  # 替换为你的MySQL密码
    'host': '127.0.0.1',  # 或者你的MySQL服务器地址
    'port': '3306',  # 默认MySQL端口是3306
}
import mysql.connector

# 假设已有MySQL服务器运行在本地，用户名为'root'，密码为'password'
# 尝试连接MySQL服务器并创建名为'ai_data'的数据库
try:
    # 连接MySQL服务器
    connection = mysql.connector.connect(**config)

    # 创建cursor对象
    cursor = connection.cursor()

    # 创建数据库的SQL语句
    create_db_query = "CREATE DATABASE IF NOT EXISTS ai_data"

    # 执行SQL语句
    cursor.execute(create_db_query)

    # 提交更改
    connection.commit()

    # 输出结果
    result = "数据库 'ai_data' 创建成功！"
except mysql.connector.Error as error:
    result = f"数据库创建失败: {error}"
finally:
    # 关闭cursor和连接
    if connection.is_connected():
        cursor.close()
        connection.close()
        result += " 已关闭连接。"

print(result)
