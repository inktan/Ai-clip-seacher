from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent import pywsgi  
import sqlite3
import random
import logging
from functools import wraps
import time 
from flask import g

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('run_flask_cmd_random_5001.log'),  # 日志文件名
        logging.StreamHandler()  # 控制台输出
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path.startswith('/random_image'):
        elapsed_time = time.time() - g.start
        logger.info(f'{request.remote_addr} - - [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] '
                    f'"{request.method} {request.path} {request.environ.get("SERVER_PROTOCOL")}" '
                    f'{response.status_code} {response.content_length} 请求耗时 {elapsed_time:.6f} s')
    return response

# db_path = 'Y:/GOA-AIGC/98-goaTrainingData/Arch_200px_/stored_paths.db'
# db = sqlite3.connect(db_path)
# table_name_data_normal = 'data_normal'
# count = db.execute(f'SELECT COUNT(PATH) FROM {table_name_data_normal} WHERE path IS NOT NULL').fetchone()[0]

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

def random_images(n: int = 300):
    '''随机选择300个图片'''
    if count < 300:
        # SQL查询语句
        query = "SELECT PATH, thumbnail_width, thumbnail_height FROM thumbnails"
        # 执行查询
        cursor.execute(query)
        # 获取所有结果
        results = cursor.fetchall()
        return results

        # image_paths = cursor.execute(f"SELECT  PATH, thumbnail_width, thumbnail_height  FROM {table_name_data_normal}").fetchall()  
        # return image_paths
    else:
        # 生成300个随机整数索引
        random_indices = random.sample(range(count), n)
        ids_str = ','.join(map(str, random_indices))  

        # SQL查询语句，随机取出300行数据
        # query = f"""
        # SELECT PATH, thumbnail_width, thumbnail_height
        # FROM thumbnails
        # ORDER BY RAND()
        # LIMIT {n}
        # """
        query = f"""
        SELECT PATH, thumbnail_width, thumbnail_height
        FROM thumbnails
        WHERE id IN ({ids_str})
        """
        # 执行查询
        cursor.execute(query)
        # 获取所有结果
        results = cursor.fetchall()
        return results

        # 使用这些索引从image_paths中提取一个新的列表
        # random_image_paths = [image_paths[i] for i in random_indices]
        # 从列表中随机选择300个图片路径

        # rows = db.execute(f'''
        #     SELECT PATH, thumbnail_width, thumbnail_height  
        #     FROM {table_name_data_normal} 
        #     WHERE ID IN ({ids_str})
        #     ''').fetchall()  
        # random_image_paths = rows
        # return random_image_paths
def run():
    @app.route('/random_image',methods=['GET'])
    def random_image():
        query_count_str = request.args.get('query_count', default=1, type=str)
        try:
            query_count = int(query_count_str)
        except ValueError:
            return "query_count must be an integer", 400
        print(query_count)
        result = random_images(n=query_count)
        # print(result)
        return jsonify(results=result)

    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    print("Searcher Serving on port 10.1.12.30:5001 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()





