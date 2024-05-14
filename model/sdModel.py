import json
import requests as rt
import random
from datetime import datetime
class sdModels(object):
    def __ini__(self):
        pass

    @classmethod
    def generate_time_related_random_string(length=8):
        # 使用当前时间作为种子
        now = datetime.now().timestamp()
        random.seed(now)
        # 字符集包括小写字母和数字
        char_set = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choices(char_set, k=length))
    @classmethod
    def sdImage(cls,mtext):
        payload = {
            "num_inference_steps":31,
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
            "prompt": mtext,     #  提示词
            # "styles": [
            #   "string"
            # ],
            "seed": -1,
             "samples":4,
            # "subseed": -1,
            # "subseed_strength": 0,
            # "seed_resize_from_h": -1,
            # "seed_resize_from_w": -1,
            # "sampler_name": "string",
            # "batch_size": 4,
            # "n_iter": 1,
            "steps": 30,
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
                                #   }
            # }
            }

        
        url = "http://127.0.0.1:1080/sdapi/v1/txt2img"
        
       # print("testing==============",payload)
        response = rt.post(url=url, json=payload)
        # print(response.json())
        r = response.json()
        return r
    
sdModel = sdModels()
