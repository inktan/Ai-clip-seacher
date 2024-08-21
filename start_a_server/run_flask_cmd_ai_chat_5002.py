from flask import Flask, Response,request, jsonify
from decorator import timer_decorator
from flask_cors import CORS
from gevent import pywsgi  

from zhipuai import ZhipuAI

app = Flask(__name__)
CORS(app)
client = ZhipuAI(api_key="6afaa8e936bc8982b107416a390216e3.sSW4FmE17ZKIVldh") # 到期时间：2024-08-29

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
    
def run():
    print("Waiting for server to start ...")

    # 暂时web前端使用fetch进行ai对话
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

    server = pywsgi.WSGIServer(('0.0.0.0', 5002), app)
    print("Searcher Serving on port 10.1.12.30:5002 ...")

    server.serve_forever()

if __name__ == "__main__":
    run()





