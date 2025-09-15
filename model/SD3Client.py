import asyncio
import aiohttp
from PIL import Image
import io
import json
import requests 
import base64
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
    async def fetch_image(self, session, server_address, payload):
        image_url = "https://www.superimage.ai/app/api/v1/prompts/generate-image-batch-tg"
        print("flag===xxx==xxx==xx==", image_url, payload)

        headers = {
            "Content-Type": "application/json"
        }

        async with session.post(image_url, json=payload, headers=headers) as response:
            # 处理JSON响应
            result = await response.json()
            print("API Response:", str(result)[:100])

            if result.get("success") and result.get("results"):
                for model_result in result["results"]:
                    if model_result.get("imageData"):
                        b64_data = model_result["imageData"]
                        image_data = base64.b64decode(b64_data)
                        image_stream = io.BytesIO(image_data)
                        image = Image.open(image_stream)
                        water_mask = "SuperImageAI"
                        return addWM.process(image, water_mask)

            # 如果没有找到图片数据，返回None
            return None

    async def fetch_images(self, prompt):
        images = []
        payload = {
            "prompt": prompt,
            "models": ["FLUX.1-dev"]
        }

        async with aiohttp.ClientSession() as session:
            # 由于新接口是批量生成，我们只需要调用一次
            tasks = [asyncio.create_task(self.fetch_image(session, server_adress, payload)) for server_adress in self.server_adresses]
            results = await asyncio.gather(*tasks)
            print("========flag2==============", len(results))

            # 过滤掉None结果并收集图片
            for result in results:
                if result is not None:
                    images.append(result)

            # 如果需要4张图片但返回不足，可以重复调用
            while len(images) < 4 and len(images) > 0:
                tasks = [asyncio.create_task(self.fetch_image(session, server_adress, payload)) for server_adress in self.server_adresses]
                additional_results = await asyncio.gather(*tasks)
                for result in additional_results:
                    if result is not None and len(images) < 4:
                        images.append(result)

            print("========flag3======", len(images))
        return images[:4]  # 确保最多返回4张图片
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
