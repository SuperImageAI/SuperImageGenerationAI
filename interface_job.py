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
import json
import requests as rt
import io
import base64
from model.sdModel import sdModel
from PIL import Image, ImageDraw, ImageFont
from model.addWaterMask import addWM
   
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
    if len(r)>0:
         
        res={ "code":0,
            "status": "success",
            "imageUrl":r
        }
    else:
        res={ "code":-1,
            "status": "failed",
            "imageUrl":r
        } 
    return json.dumps(res, ensure_ascii=False)

def post_task(param):
        """解析请求中的参数，识别完成后返回识别结果"""
        print("run函数有执行")
        print(param)
        text = param['prompt']
       # test = addWM()
        imageUrl =''
        try:
            r = sdModel.sdImage(text)
            image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        # image.resize((10,10))
            print("=====flag1=====")
            current_dir = os.getcwd()
            imName= sdModel.generate_time_related_random_string(16)
            imPath = current_dir+'/photos/'+imName+'.png'
            water_mask = "SuperImageAI"
            image = addWM.process(image, water_mask)
            image.save(imPath)
            imageUrl=imPath
        except:
             print("生成图片失败!")

        return  imageUrl

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # 启动http api
    app.run(debug=False, host=get_host_ip(), port=1088)















