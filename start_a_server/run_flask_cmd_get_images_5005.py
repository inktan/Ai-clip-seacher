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
    searcher = Search(image_dir_path = r'Y:\GOA-AIGC\98-goaTrainingData\ArchOctopus_thumbnail_200px',
                traverse= False,
                save_path = '',
                reindex = False,)

    print("Waiting for server to start ...")
    
    @app.route('/get_best_images_prompt',methods=['POST'])
    def get_best_images_prompt():
        try:
            prompt = request.form.get("prompt")
            print(f"User query: {prompt}")
            # 中译英
            try:
                prompt = baidu_text_trans(prompt)
                print(f"User query: {prompt}")
            except Exception as e:
                prompt = request.form.get("prompt")
                
            imageWeight =  request.form.get('imageWeight')
            imageWeight = float(imageWeight)
            
            prompt_img = request.files.get('prompt_img')
            if prompt_img and prompt_img.filename != '':  
                print(f"User query image: { prompt_img.filename}")
                prompt_img = Image.open(io.BytesIO(prompt_img.read()))
            else:
                imageWeight=0
            print(f"User query imageWeight: {imageWeight}")

            n01 =  request.form.get("n01")
            n01= int(n01)
            print(f"query count: {n01}")
            n02 =  request.form.get("n02")
            n02= int(n02)
            print(f"query count: {n02}")

            # result = searcher.rank_images_by_query_sqlite_image(imageWeight,prompt, prompt_img, n01, n02)
            result = searcher.rank_images_by_query_image(imageWeight,prompt, prompt_img, n01, n02)
            
            response_data = {
                'prompt': prompt,
                'results': result
            }

            return jsonify(response_data)
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)

    server = pywsgi.WSGIServer(('0.0.0.0', 5005), app)
    print("Searcher Serving on port 10.1.12.30:5005 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()

