import asyncio
import aiohttp
from PIL import Image
import io
import json
# import base64
from addWaterMask import addWM
from getSD3Image import getSDImage
import random
import uuid

class SD3Client:
    def __init__(self, server_addresses):
        self.server_adresses = server_addresses
        self.client_id = str(uuid.uuid4())
   # def queue_prompt(prompt):
    #     p = {"prompt": prompt, "client_id": client_id}
    #     data = json.dumps(p).encode('utf-8')
    #     req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    #     return json.loads(urllib.request.urlopen(req).read())
    async def fetch_image(self, session, server_address,client_id ,payload):
        # payload["271"]["inputs"]["seed"] =random.randint(1, 945512652412924)
        p = {"prompt": payload, "client_id": client_id}
        # data = json.dumps(p).encode('utf-8') 
        url = "http://{}/prompt".format(server_address)
        print("flag===xxx==",url,p)
        headers = {"Content-Type": "application/json"}
        async with session.post(url, json=p,headers=headers) as response:
            print(response,type(response))
            r = await response.json()
            # client_id = self.client_id
            getImge = getSDImage(server_address=server_address,client_id=client_id,rdata=r)
            image_data = getImge.get_images()
            print("image_data=======",len(image_data))
            image = Image.open(io.BytesIO(image_data))
            water_mask = "SuperImageAI"
            # image = addWM.process(image, water_mask)
            return  addWM.process(image, water_mask)

    async def fetch_images(self, prompt):
        with open("fluxworkflow.json","r",encoding="utf-8") as f:
            workflow_jsondata = f.read()
        client_id = self.client_id
        payload = json.loads(workflow_jsondata)
        # random_integer = random.randint(-100000, 100000)
        payload["6"]["inputs"]["text"] = prompt
        images = []

        async with aiohttp.ClientSession() as session:
            for kk in range(2):
                tasks = [asyncio.create_task(self.fetch_image(session, server_adress, client_id,payload)) for server_adress in self.server_adresses]
                results = await asyncio.gather(*tasks)
                print("========flag2==============",len(results))
                for result in results:
                    images.append(result)
                    # print("========flag3======",result.get("images", []))
            print("========flag3======",len(images))
        return images
# sdClient = StableDiffusionClient() 
# 使用示例
# async def main():
#     # 定义两个HTTP服务的URL
#     urls = [
#         "http://127.0.0.1:1080/sdapi/v1/txt2img",
#         "http://127.0.0.1:1081/sdapi/v1/txt2img"
#     ]
#     client = StableDiffusionClient(urls)
#     images = await client.fetch_images("你的文本提示")
    
#     # 打印或处理图片列表
#     print(images)

# # 运行异步主函数
# asyncio.run(main())
