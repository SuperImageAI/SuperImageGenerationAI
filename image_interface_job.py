# -*- coding: utf-8 -*-
"""
 @FileName: img_to_words_api.py
"""
from flask import Flask, request
import socket
import json
# from model_set.rule_parse import 
from io import BytesIO
import io
import os
import json
import requests as rt
import base64
from model.sd3Model import sd3Models
from PIL import Image, ImageDraw, ImageFont
from model.addWaterMask import addWM
from model.registerModel import registerModel
# current_path = abspath(dirname(__file__))
#
# root_path = current_path.replace("/ocr/main", "")
#
# sys.path.append(root_path)
#
app = Flask(__name__)
model_name = '/v1/images/generations'

@app.route(model_name, methods=['POST'])

def post():

    param = request.json

    print(param)
    print("post1有执行")
    current_dir =  os.path.dirname(__file__)
    config_file_path =current_dir +"/config/config.py"
    print("config_file_path======",config_file_path)
    regModel=registerModel(config_file_path) 
    current_status = regModel.read_register_status()

    if current_status==0:
        regModel.registerProcess()
        current_status = regModel.read_register_status()
    
    if current_status==1:
         
        r = post_task(param)
        print(r)
        if len(r)>0:
         
            res={ "code":0,
                "message": "success",
                "created": 1589478378,
                "data":r
            }
        else:
            res={ "code":-1,
                "message": "failed",
                "data":r
            } 
    else:
        res={ "code":-1,
                "message": "model register failed",
                "data":[]
            }  
    return json.dumps(res, ensure_ascii=False)

def post_task(param):
        """解析请求中的参数，识别完成后返回识别结果"""
        print("run函数有执行")
        print(param)
        text = param['prompt']
        Num = param['n']
        # test = addWM()
        data =[]
        try:

            server_address ="127.0.0.1:8188"
            sdmodel = sd3Models(server_address,16)
            for k in range(Num):
                image_data = sdmodel.sd3Image(text)
                image = Image.open(io.BytesIO(image_data))
                water_mask = "SuperImageAI"
                image = addWM.process(image, water_mask)
            # image.resize((10,10))
                print("=====flag1=====")
                current_dir = os.getcwd()
                imName= sdmodel.generate_time_related_random_string()
                imageUrl = current_dir+'/photos/'+imName+'.png'
                imageInfo ={}
                imageInfo["url"]=imageUrl
                image.save(imageUrl)
                data.append(imageInfo)
        except:
             print("生成图片失败!")

        return  data

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # 启动http api
    app.run(debug=False, host=get_host_ip(), port=1088)















