from flask import Flask, Response,request, jsonify
from PIL import Image
import requests,base64
from flask_cors import CORS
from gevent import pywsgi  
from PIL import Image
from io import BytesIO
import logging
import time 
from flask import g

from zhipuai import ZhipuAI

import configparser
config_file_path = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file_path)
api_credentials = {
    'api_key': config.get('ZhipuAI_api_credentials', 'api_key'),
    'expiration_date': config.get('ZhipuAI_api_credentials', 'expiration_date')
}

client = ZhipuAI(api_key=api_credentials['api_key'])

def zhipuai_read_image(base64_image_data,is_stream=False):
    # image_bytes = BytesIO()
    # img.save(image_bytes, format=img.format)
    # image_bytes = image_bytes.getvalue()

    # base64_image_data = base64.b64encode(image_bytes).decode('utf-8')

    img_info={
        # 'img_path':img_path,
        'base64_image_data':base64_image_data,
    }
    response = client.chat.completions.create(
    #   model="glm-4",  # 填写需要调用的模型名称
    model="glm-4v",  # 填写需要调用的模型名称
        messages=[
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "你是一个聪明且富有创造力的建筑设计师，请详细描述图的建筑特征"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_info['base64_image_data']}"
                }
            }
            ]
        }
        ],
        stream=is_stream,
        )
    if is_stream:
        for chunk in response:
            # print(chunk.choices[0].delta.content)
            yield chunk.choices[0].delta.content
    else:
        answer = response.choices[0].message.content
        # print(answer)
        return answer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('run_flask_cmd_ai_image_descri_5003.log'),  # 日志文件名
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
    if request.path.startswith('/ai_image_description'):
        elapsed_time = time.time() - g.start
        logger.info(f'{request.remote_addr} - - [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] '
                    f'"{request.method} {request.path} {request.environ.get("SERVER_PROTOCOL")}" '
                    f'{response.status_code} {response.content_length} 请求耗时 {elapsed_time:.6f} s')
    return response

def run():
    print("Waiting for server to start ...")
    
    @app.route('/ai_image_description',methods=['GET'])
    def ai_image_description():
        img_url = request.args.get('img_url')
        try:
            print(f"User proinfo_img: { img_url}")
            response = requests.get(img_url)
            response.raise_for_status() # 如果请求失败，将抛出HTTPError异常

            proinfo_img =Image.open(BytesIO(response.content))

            image_bytes = BytesIO()
            proinfo_img.save(image_bytes, format=proinfo_img.format)
            image_bytes = image_bytes.getvalue()

            base64_image_data = base64.b64encode(image_bytes).decode('utf-8')
            # answer = zhipuai_read_image(base64_image_data, False)
            # result = [answer]
            # return jsonify(results=result)
        
            return Response(zhipuai_read_image(base64_image_data, True), mimetype='text/event-stream')

        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)

    server = pywsgi.WSGIServer(('0.0.0.0', 5003), app)
    print("Searcher Serving on port 10.1.12.30:5003 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()





