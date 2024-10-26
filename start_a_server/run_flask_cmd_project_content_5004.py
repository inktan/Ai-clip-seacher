from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent import pywsgi  
import sqlite3
import logging
import time 
from flask import g

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('run_flask_cmd_project_content_5004.log'),  # 日志文件名
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
    if request.path.startswith('/project_content'):
        elapsed_time = time.time() - g.start
        logger.info(f'{request.remote_addr} - - [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] '
                    f'"{request.method} {request.path} {request.environ.get("SERVER_PROTOCOL")}" '
                    f'{response.status_code} {response.content_length} 请求耗时 {elapsed_time:.6f} s')
    return response

db_path = r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus_thumbnail_200px\stored_paths.db'
db = sqlite3.connect(db_path)
table_name_data_normal = 'data_normal'
count = db.execute(f'SELECT COUNT(PATH) FROM {table_name_data_normal} WHERE path IS NOT NULL').fetchone()[0]

def get_project_content(project_path):
    '''获取一个项目的所有相关信息'''

    rows = db.execute(f'''
        SELECT * 
        FROM {table_name_data_normal} 
        WHERE PATH LIKE '%{project_path}%'
        ''').fetchall()  
    filtered_list = [tup[1] for tup in rows]  

    return filtered_list

def run():
    print("Waiting for server to start ...")

    @app.route('/project_content',methods=['GET'])
    def project_content():
        project_path = request.args.get("project_path") 
        result = get_project_content(project_path)
        return jsonify(results=result)

    server = pywsgi.WSGIServer(('0.0.0.0', 5004), app)
    print("Searcher Serving on port 10.1.12.30:5004 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()





