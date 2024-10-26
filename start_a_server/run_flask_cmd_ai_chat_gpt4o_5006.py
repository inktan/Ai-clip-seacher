from flask import Flask, Response,request, jsonify
from flask_cors import CORS
from gevent import pywsgi  
import logging
import time 
from flask import g

import json
import requests
import time
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('run_flask_cmd_ai_chat_gpt4o_5006.log'),  # 日志文件名
        logging.StreamHandler()  # 控制台输出
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有来源的跨
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path.startswith('/ai_chat'):
        elapsed_time = time.time() - g.start
        logger.info(f'{request.remote_addr} - - [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] '
                    f'"{request.method} {request.path} {request.environ.get("SERVER_PROTOCOL")}" '
                    f'{response.status_code} {response.content_length} 请求耗时 {elapsed_time:.6f} s')
    return response

headers = {
# 'Authorization': 'Bearer fk192489-7dCTdBKwtYid3GzzAvy3om3gVEwSRBNU',
'Authorization': 'Bearer fk192612-pLVI3zuqAZCoCaeeDaZqmhia1uHmz4RE',
'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
'Content-Type': 'application/json'
}

url = "https://oa.api2d.net/v1/chat/completions"

def run():
    print("Waiting for server to start ...")

    # 暂时web前端使用fetch进行ai对话
    @app.route('/ai_chat',methods=['POST'])
    def ai_chat():
        messageList = request.json
        payload = json.dumps({
        "model": "gpt-4o",
        #    "model": "gpt-3.5-turbo",
        "messages": messageList['messages'],
            # "max_tokens":300,
            "safe_mode": False
        })

        while True:     
            try:         
                response = requests.request("POST", url, headers=headers, data=payload)
                converted_dict = json.loads(response.text)
                text = converted_dict['choices'][0]['message']['content']
                return jsonify(content=text)
                # return text
                
            except  Exception as e:
                print(e)
                print("Connection error. Trying again in 2 seconds.")
                time.sleep(2)

    @app.route('/ai_chat_get',methods=['GET'])
    def ai_chat_get():
        try:         
            return jsonify(content='text success')
            # return text
            
        except  Exception as e:
            print(e)
            print("Connection error. Trying again in 2 seconds.")
            time.sleep(2)

    server = pywsgi.WSGIServer(('0.0.0.0', 5006), app)
    print("Searcher Serving on port 10.1.12.30:5006 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()

