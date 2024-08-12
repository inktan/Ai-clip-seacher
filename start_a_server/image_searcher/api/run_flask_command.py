from typing import Optional
from flask import Flask, request, jsonify ,send_file
from flask_cors import CORS
from image_searcher import Search
from image_searcher.api.flask_config import FlaskConfig
from gevent import pywsgi  
from PIL import Image
import io, time, yaml, logging
from functools import wraps
from image_searcher.api.Baidu_Text_transAPI import baidu_text_trans

def timer_decorator(func):
    """装饰器，用于计算函数运行的时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 运行耗时: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

class RunFlaskCommand:
    logging.basicConfig(level=logging.INFO)

    @timer_decorator
    def __init__(self, config_path: Optional[str] = None, searcher: Optional[Search] = None):
        if config_path is None and searcher is None:
            raise AttributeError("Either the config path or the searcher need to be defined")

        self.searcher = searcher
        if config_path:
            self.config = FlaskConfig(**yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader))
        else:
            self.config = FlaskConfig(image_dir_path=self.searcher.loader.image_dir_path,
                                      traverse=self.searcher.loader.traverse,
                                      save_path=self.searcher.stored_embeddings.save_path,
                                      reindex=False,
                                      include_faces=len(self.searcher.stored_embeddings.face_embedding_paths) > 0)

    @timer_decorator
    def get_best_images_prompt(self):
        '''路由 文搜图'''
        # 参数-提示词
        # 参数-图像
        # 参数-图像权重
        try:
            prompt = request.form.get("prompt")
            logging.info(f"User query: {prompt}")
            # 中译英
            try:
                prompt = baidu_text_trans(prompt)
                logging.info(f"User query: {prompt}")
            except Exception as e:
                prompt = request.form.get("prompt")
                
            imageWeight =  request.form.get('imageWeight')
            imageWeight = float(imageWeight)
         
            prompt_img = request.files.get('prompt_img')
            if prompt_img and prompt_img.filename != '':  
                logging.info(f"User query image: { prompt_img.filename}")
                prompt_img = Image.open(io.BytesIO(prompt_img.read()))
            else:
                imageWeight=0
            logging.info(f"User query imageWeight: {imageWeight}")

            n01 =  request.form.get("n01")
            n01= int(n01)
            logging.info(f"query count: {n01}")
            n02 =  request.form.get("n02")
            n02= int(n02)
            logging.info(f"query count: {n02}")

            result = self.searcher.rank_images_by_query_image(imageWeight,prompt, prompt_img, n01, n02)
            
            # 创建一个字典，包含所有要发送到前端的数据
            response_data = {
                'prompt': prompt,
                'results': result
            }

            # 使用 jsonify 将字典转换为 JSON 响应
            return jsonify(response_data)
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)
    
    @timer_decorator
    def random_image(self):
        # 从查询字符串中获取 query_count 参数
        query_count_str = request.args.get('query_count', default=1, type=str)
        
        # 将 query_count 参数转换为整数
        try:
            query_count = int(query_count_str)
        except ValueError:
            # 如果转换失败，返回错误信息
            return "query_count must be an integer", 400
        print(query_count)
        result = self.searcher.random_images(n=query_count)
        return jsonify(results=result)
    
    @timer_decorator
    def project_content(self):
        project_path = request.args.get("project_path") 
        result = self.searcher.project_content(project_path)
        return jsonify(results=result)

    @timer_decorator
    def run(self, start=True):
        logging.info("Waiting for server to start ...")

        app = Flask(__name__, static_folder=None)
        self.searcher = Search(image_dir_path=self.config.image_dir_path,
                               traverse=self.config.traverse,
                               save_path=self.config.stroed_embeddings_save_path,
                               reindex=self.config.reindex,
                               include_faces=self.config.include_faces)
        CORS(app)

        app.add_url_rule("/get_best_images_prompt", "get_best_images_prompt", self.get_best_images_prompt, methods=["POST"])
        app.add_url_rule("/random_image", "random_image", self.random_image, methods=["GET"])
        app.add_url_rule("/project_content", "project_content", self.project_content, methods=["GET"])

        if start:
            # app.run(port=self.config.port,
            #         host=self.config.host,
            #         debug=self.config.debug,
            #         threaded=self.config.threaded)
            
            # server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
            # print("Searcher Serving on port 127.0.0.1:5000 ...")
            server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
            print("Searcher Serving on port 10.1.12.30:5000 ...")

            server.serve_forever()

        return app

@timer_decorator
def run(**kwargs):
    command = RunFlaskCommand(**kwargs)
    command.run()




