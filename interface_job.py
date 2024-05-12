# -*- coding: utf-8 -*-
"""
 @FileName: img_to_words_api.py
"""
from flask import Flask, request
import socket
import json
# from model_set.rule_parse import 
from io import BytesIO
from model.sdModel import sdModel
import io
import os
import base64
from model.addWaterMask import addWM
from model.StableDiffusionClient import StableDiffusionClient

   
# current_path = abspath(dirname(__file__))
#
# root_path = current_path.replace("/ocr/main", "")
#
# sys.path.append(root_path)
#
app = Flask(__name__)
model_name = '/models/superImage/'

@app.route(model_name, methods=['POST'])

def post():

    param = request.json

    print(param)
    print("post1有执行")
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
        text = param['prompt']
        urls = [
        "http://127.0.0.1:1080/sdapi/v1/txt2img"
        # "http://127.0.0.1:1081/sdapi/v1/txt2img"
        ]
        client = StableDiffusionClient(urls)
        current_dir = os.getcwd()
        images = client.fetch_images(text)
        # image1Path=current_dir+'/photos/'+'image1.jpg'

        print("=================flag1============",images,len(images)) 

        images[0].save(current_dir+'/photos/'+'image1.jpg')
        images[1].save(current_dir+'/photos/'+'image2.jpg')
        status=0
        if len(images)==2:
             status = 1
        
        return status

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # 启动http api
    app.run(debug=False, host=get_host_ip(), port=10429)















