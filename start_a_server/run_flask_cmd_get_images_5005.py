from flask import Flask, request, jsonify
from image_searcher.api.search import Search
from PIL import Image
from image_searcher.api.Baidu_Text_transAPI import baidu_text_trans
import io
from flask_cors import CORS
from gevent import pywsgi  
from PIL import Image
import logging
import time 
from flask import g

from io import BytesIO
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('run_flask_cmd_get_images_5005.log'),  # 日志文件名
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
    if request.path.startswith('/get_best_images_prompt'):
        elapsed_time = time.time() - g.start
        logger.info(f'{request.remote_addr} - - [{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] '
                    f'"{request.method} {request.path} {request.environ.get("SERVER_PROTOCOL")}" '
                    f'{response.status_code} {response.content_length} 请求耗时 {elapsed_time:.6f} s')
    return response

def run():
    # searcher = Search(image_dir_path = 'Y:/GOA-AIGC/98-goaTrainingData/ArchOctopus',
    #             traverse= True,
    #             save_path = '',
    #             reindex = True,)
    searcher = Search(image_dir_path = 'Y:/GOA-AIGC/98-goaTrainingData/Arch_200px_',
                traverse= False,
                save_path = '',
                reindex = False,)

    # searcher = Search(image_dir_path = '',
    #             traverse= False,
    #             save_path = '',
    #             reindex = False,)

    print("Waiting for server to start ...")
    
    @app.route('/get_best_images_prompt',methods=['POST'])
    def get_best_images_prompt():
        try:
            prompt = request.form.get("prompt")
            logger.info(prompt)
            prompt_list=[]
            prompt_list.append(prompt)

            print(f"User query: {prompt}")
            # 中译英
            try:
                prompt = baidu_text_trans(prompt)
                print(f"User query: {prompt}")
            except Exception as e:
                prompt = request.form.get("prompt")
            logger.info(prompt)
            prompt_list.append(prompt)
                
            imageWeight =  request.form.get('imageWeight')
            imageWeight = float(imageWeight)
            
            prompt_img = request.files.get('prompt_img')

            if prompt_img and prompt_img.filename != '':  
                print(f"User query image: { prompt_img.filename}")
                prompt_img = Image.open(io.BytesIO(prompt_img.read()))
            else:
                imageWeight=0
            if prompt == '' or prompt.isspace():
                imageWeight=1

            print(f"User query imageWeight: {imageWeight}")

            rendering_img = request.form.get("rendering_img")
            rendering_img = True if rendering_img.lower() == 'true' else False

            realScene_img = request.form.get("realScene_img")
            realScene_img = True if realScene_img.lower() == 'true' else False

            n01 =  request.form.get("n01")
            n01= int(n01)
            print(f"query count: {n01}")
            n02 =  request.form.get("n02")
            n02= int(n02)
            print(f"query count: {n02}")

            # result = searcher.rank_images_by_query_sqlite_image(imageWeight,prompt, prompt_img, n01, n02)
            result = searcher.rank_images_by_query_image(imageWeight,prompt, prompt_img,rendering_img,realScene_img, n01, n02)
            
            response_data = {
                'prompt': prompt,
                'results': result
            }
                        
            prompt_lists.append(prompt_list)
            with open('%s' % prompts_01_csv ,'a',encoding='utf-8' ,newline='') as f:
                writer = csv.writer(f)
                writer.writerows(prompt_lists)

            return jsonify(response_data)
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)
        
    @app.route('/get_best_images',methods=['GET'])
    def get_best_image():
        try:
            prompt_list=[]

            prompt = request.args.get("prompt")
            imageWeight = request.args.get("imageWeight")
            prompt_img_url = request.args.get("prompt_img_url")
            rendering_img = request.args.get("rendering_img")
            realScene_img = request.args.get("realScene_img")
            n01 = request.args.get("n01")
            n02 = request.args.get("n02")
            
            logger.info(prompt)
            prompt_list.append(prompt)

            print(f"User query: {prompt}")
            # 中译英
            try:
                prompt = baidu_text_trans(prompt)
                print(f"User query: {prompt}")
            except Exception as e:
                prompt = request.form.get("prompt")
            logger.info(prompt)
            prompt_list.append(prompt)

            imageWeight = float(imageWeight)
            if prompt_img_url is not None and prompt_img_url != '':
                # 发送请求获取图片数据
                response = requests.get(prompt_img_url)
                # 检查请求是否成功
                if response.status_code == 200:
                    # 使用BytesIO将图片数据转换为文件对象
                    image_file = BytesIO(response.content)
                    # 使用PIL的Image.open打开图片
                    prompt_img = Image.open(image_file)
                    prompt_list.append(prompt_img_url)
                    print(f"User query image: { prompt_img_url}")
                else:
                    print(prompt_img_url, "无法获取图片，状态码：", response.status_code)
                    imageWeight=0
                    prompt_img=None
            else:
                imageWeight=0
                prompt_img=None

            print(f"User query imageWeight: {imageWeight}")

            rendering_img = True if rendering_img.lower() == 'true' else False
            realScene_img = True if realScene_img.lower() == 'true' else False

            n01= int(n01)
            print(f"query count: {n01}")
            n02= int(n02)
            print(f"query count: {n02}")

            result = searcher.rank_images_by_query_image(imageWeight,prompt, prompt_img,rendering_img,realScene_img, n01, n02)
            
            response_data = {
                # 'prompt': prompt,
                'results': result
            }
                        
            prompt_lists.append(prompt_list)
            with open('%s' % prompts_01_csv ,'a',encoding='utf-8' ,newline='') as f:
                writer = csv.writer(f)
                writer.writerows(prompt_lists)

            return jsonify(response_data)
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)

    @app.route('/search_by_picUrl',methods=['POST'])
    def search_by_picUrl():
        try:
            prompt_list=[]
            
            prompt = request.form.get("prompt")
            logger.info(prompt)
            prompt_list.append(prompt)
            
            imageWeight =  request.form.get('imageWeight')
            imageWeight = float(imageWeight)

            prompt_img_url = request.form.get('prompt_img_url')
            # 发送请求获取图片数据
            response = requests.get(prompt_img_url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 使用BytesIO将图片数据转换为文件对象
                image_file = BytesIO(response.content)
                # 使用PIL的Image.open打开图片
                prompt_img = Image.open(image_file)
                prompt_list.append(prompt_img_url)
                print(f"User query image: { prompt_img_url}")
            else:
                print("无法获取图片，状态码：", response.status_code)
                imageWeight=0

            print(f"User query imageWeight: {imageWeight}")

            rendering_img = request.form.get("rendering_img")
            rendering_img = True if rendering_img.lower() == 'true' else False

            realScene_img = request.form.get("realScene_img")
            realScene_img = True if realScene_img.lower() == 'true' else False

            n01 =  request.form.get("n01")
            n01= int(n01)
            print(f"query count: {n01}")
            n02 =  request.form.get("n02")
            n02= int(n02)
            print(f"query count: {n02}")

            # result = searcher.rank_images_by_query_sqlite_image(imageWeight,prompt, prompt_img, n01, n02)
            result = searcher.rank_images_by_query_image(imageWeight,prompt, prompt_img,rendering_img,realScene_img, n01, n02)
            
            response_data = {
                'prompt': prompt,
                'results': result
            }
                        
            prompt_lists.append(prompt_list)
            with open('%s' % prompts_01_csv ,'a',encoding='utf-8' ,newline='') as f:
                writer = csv.writer(f)
                writer.writerows(prompt_lists)

            return jsonify(response_data)
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)

    server = pywsgi.WSGIServer(('0.0.0.0', 5005), app)
    print("Searcher Serving on port 10.1.12.30:5005 ...")

    server.serve_forever()

import os
import csv

prompt_lists = []
prompts_01_csv= os.path.join(r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus',"prompts_01.csv")

with open('%s' % prompts_01_csv ,'a',encoding='utf-8' ,newline='') as f:
    writer = csv.writer(f)
    writer.writerows(prompt_lists)

if __name__ == "__main__":
    run()

