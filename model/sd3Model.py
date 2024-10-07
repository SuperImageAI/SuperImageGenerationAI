import json
import requests as rt
import random
from datetime import datetime
from model.getSD3Image import getSDImage
import random
import uuid
import os
class sd3Models:
    def __init__(self, server_address,length):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.length =length
    
    def generate_time_related_random_string(self):
        # 使用当前时间作为种子
        now = datetime.now().timestamp()
        random.seed(now)
        # 字符集包括小写字母和数字
        char_set = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choices(char_set, k=self.length))
    
    def sd3Image(self,mtext):
        current_dir = os.path.dirname(__file__)
        # with open(current_dir+"/"+"workflow_api.json","r",encoding="utf-8") as f:
        #     workflow_jsondata = f.read()
        
        # client_id =self.client_id
        # server_address=self.server_address
        # payload = json.loads(workflow_jsondata)
        # payload["6"]["inputs"]["text"] = mtext
        # payload["271"]["inputs"]["seed"] =random.randint(1, 945512652412924)
        # p = {"prompt": payload, "client_id": client_id}
        # data = json.dumps(p).encode('utf-8')
        payload = {} 
        payload["prompt"]= prompt
        payload["size"]="1024x1024"
        payload["model"] = "FLUX.1-dev" 
        url = "http://{}/v1/images/generations".format(server_address)
        print("flag===xxx==",url,payload)
        headers = {"Content-Type": "application/json"}
        with rt.post(url, json=payload,headers=headers) as response:
            print(response,type(response))
            r =  response.json()
        
        imag_url = r["url"]
            # client_id = self.client_id
            # getImge = getSDImage(server_address=server_address,client_id=client_id,rdata=r)
            # image_data = getImge.get_images()
        res = rt.get(url)
        image_data = io.BytesIO(res.content)
         # client_id = self.client_id
        # getImge = getSDImage(server_address=server_address,client_id=client_id,rdata=r)
        # image_data = getImge.get_images()
        print("image_data=======",len(image_data))
        return image_data
    

