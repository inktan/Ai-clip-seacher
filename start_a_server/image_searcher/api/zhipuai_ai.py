import os,io,json,requests,time,base64,logging
from flask import Flask, Response,request, jsonify
from flask_cors import CORS
from gevent import pywsgi  
from PIL import Image
from functools import wraps
from io import BytesIO

from zhipuai import ZhipuAI

client = ZhipuAI(api_key="6afaa8e936bc8982b107416a390216e3.sSW4FmE17ZKIVldh") # 请填写您自己的APIKey

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

def zhipuai_chat(messageList, is_stream=False):
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        # model="glm-4v",  # 填写需要调用的模型名称
        messages = messageList,
        stream = is_stream,
        )
    if is_stream:
        for chunk in response:
            print(chunk.choices[0].delta.content)
            yield chunk.choices[0].delta.content
    else:
        answer = response.choices[0].message.content
        # print(answer)
        return answer

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
    @timer_decorator
    def ai_chat(self):
        try:
            messageList = request.json
            return Response(zhipuai_chat(messageList, True), mimetype='text/event-stream')
        except Exception as e:
            print(e)
            result = [str(e)]
            return jsonify(results=result)
    
    @timer_decorator
    def ai_image_description(self):
        img_url = request.args.get('img_url')
        try:
            logging.info(f"User proinfo_img: { img_url}")
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

    @timer_decorator
    def run(self, start=True):
        logging.info("Waiting for server to start ...")

        app = Flask(__name__, static_folder=None)
        CORS(app)

        app.add_url_rule("/ai_chat", "ai_chat", self.ai_chat, methods=["POST"])
        app.add_url_rule("/ai_image_description", "ai_image_description", self.ai_image_description, methods=["GET"])
        if start:
            server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
            print("Searcher Serving on port http://10.1.12.30:5001 ...")
            server.serve_forever()

        return app

def run(**kwargs):
    command = RunFlaskCommand(**kwargs)
    command.run()

if __name__ == "__main__":
    run()


