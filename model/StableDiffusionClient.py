import asyncio
import aiohttp
from PIL import Image
import io
import base64
from model.addWaterMask import addWM
class StableDiffusionClient:
    def __init__(self, urls):
        self.urls = urls

    async def fetch_image(self, session, url, payload):
        async with session.post(url, json=payload) as response:
            r = await response.json()
            image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
            water_mask = "SuperImageAI"
            # image = addWM.process(image, water_mask)
            return  addWM.process(image, water_mask)

    async def fetch_images(self, prompt, num_images_per_service=2):
        # payload = {
        #     "prompt": prompt,
        #     "num_images": num_images_per_service
        # }
        payload = {
            "num_inference_steps":15,
            # "enhance_prompt":'yes',
            # "enable_hr": False,
            # "denoising_strength": 0,
            # "firstphase_width": 0,
            # "firstphase_height": 0,
            # "hr_scale": 2,
            # "hr_upscaler": "string",
            # "hr_second_pass_steps": 0,
            # "hr_resize_x": 0,
            # "hr_resize_y": 0,
            "prompt": prompt,     #  提示词
            "num_images": num_images_per_service,
            # "styles": [
            #   "string"
            # ],
            "seed": -1,
            # "subseed": -1,
            # "subseed_strength": 0,
            # "seed_resize_from_h": -1,
            # "seed_resize_from_w": -1,
            # "sampler_name": "string",
            # "batch_size": 1,
            # "n_iter": 1,
            "steps": 15,
            "cfg_scale": 10,
            "width": 1024,
             "height": 1024,
            "restore_faces": 'true',
            # "tiling": False,
            # "do_not_save_samples": False,
            # "do_not_save_grid": False,
            "negative_prompt": "worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D ,3D Game, 3D Game Scene, 3D Character:1.1), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3), poorly drawn face mutation deformed ugly cloned face missing lips ugly face missing limbs amputee disfigured tentacles",
            # "eta": 0,
            # "s_churn": 0,
            # "s_tmax": 0,
            # "s_tmin": 0,
            # "s_noise": 1,
            # "override_settings": {},
            # "override_settings_restore_afterwards": True,
            # "script_args": [],
            "sampler_index": "Euler a",
            # "script_name": "string"
            # "send_images": True,
            # "save_images": True,
            # "alwayson_scripts": { "ADetailer": {
            #           "args": [{ "ad_model": "hand_yolov8n.pt"},
            #                         { "ad_model": "face_yolov8n.pt" }
            #                      ]
            #                       }
            # }
            }

        images = []

        async with aiohttp.ClientSession() as session:
            for kk in range(2):
                tasks = [asyncio.create_task(self.fetch_image(session, url, payload)) for url in self.urls]
                results = await asyncio.gather(*tasks)
                print("========flag2==============",results,len(results))
                for result in results:
                    images.append(result)
                    # print("========flag3======",result.get("images", []))
            print("========flag3======",images,len(images))
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
