from flask import Flask, Response,request, jsonify, render_template,send_from_directory
from image_searcher.api.search import Search
from PIL import Image
from image_searcher.api.Baidu_Text_transAPI import baidu_text_trans
from image_searcher.api.zhipuai_ai import zhipuai_read_image,zhipuai_chat
from decorator import timer_decorator
import requests,base64,io,os
from flask_cors import CORS
from gevent import pywsgi  
from PIL import Image
from io import BytesIO

def run():
    searcher = Search(image_dir_path = '',
                traverse= False,
                save_path = '',
                reindex = False,)

    print("Waiting for server to start ...")
    
    app = Flask(__name__, static_folder=r'D:\Users\wang.tan\Documents\GitHub\Ai-clip-seacher\Ai-clip-seacher\dist')
    CORS(app)

    @app.route('/')
    @timer_decorator
    def index():
        return send_from_directory(app.static_folder, 'index.html') 
    
    # 路由用于提供位于 'assets' 子文件夹中的静态文件
    @app.route('/assets/<path:filename>')
    @timer_decorator
    def assets(filename):
        # 指定 'assets' 子文件夹的完整路径
        full_path = os.path.join(app.static_folder, 'assets')
        return send_from_directory(full_path, filename)

    @app.route('/get_best_images_prompt',methods=['POST'])
    # @timer_decorator
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

            result = searcher.rank_images_by_query_sqlite_image(imageWeight,prompt, prompt_img, n01, n02)
            
            response_data = {
                'prompt': prompt,
                'results': result
            }

            return jsonify(response_data)
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)

    @app.route('/random_image',methods=['GET'])
    @timer_decorator
    def random_image():
        query_count_str = request.args.get('query_count', default=1, type=str)
        try:
            query_count = int(query_count_str)
        except ValueError:
            return "query_count must be an integer", 400
        print(query_count)
        result = searcher.random_images(n=query_count)
        return jsonify(results=result)

    @timer_decorator
    @app.route('/project_content',methods=['GET'])
    def project_content():
        project_path = request.args.get("project_path") 
        result = searcher.project_content(project_path)
        return jsonify(results=result)

    @app.route('/ai_chat',methods=['POST'])
    @timer_decorator
    def ai_chat():
        try:
            messageList = request.json
            return Response(zhipuai_chat(messageList, True), mimetype='text/event-stream')
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)

    @app.route('/ai_image_description',methods=['GET'])
    @timer_decorator
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

    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    print("Searcher Serving on port 10.1.12.30:5001 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()





