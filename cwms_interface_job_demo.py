# -*- coding: utf-8 -*-

"""
 @FileName: img_to_words_api.py
"""
import socket
from gevent.pywsgi import WSGIServer
from gevent import monkey
import json
from flask import Flask, request, jsonify
from model_set.rule_parse import Rule_Parse

# monkey.patch_all()

# current_path = abspath(dirname(__file__))
#
# root_path = current_path.replace("/ocr/main", "")
#
# sys.path.append(root_path)
#
app = Flask(__name__)
model_name = '/models/cwms_shelve/'

@app.route(model_name, methods=['POST'])


def post():

    param = request.json

    # print(param)
    # print("post1有执行")
    r = post_task(param)

    print(r)

    res={ "code":0,
        "count": 0,
        "data": 'true',
        "msg": "success",
        "data":r
    }

    return json.dumps(res, ensure_ascii=False)

def post_task(param):
    """解析请求中的参数，识别完成后返回识别结果"""
    print("run函数有执行")
    print(param)
    result = Rule_Parse.run(Rule_Parse,param)
    return result

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # 启动http api
    # app.run(debug=False, host=get_host_ip(), port=10429,threaded=True)
    http_server = WSGIServer(('0.0.0.0', 10537), app)
    http_server.serve_forever()















