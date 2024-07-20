
# 假设 config.py 文件内容如下：
# registerStatus = 0

import re
import requests as rt

class registerModel:
    def __init__(self, config_file_path):
        self.config_file_path=config_file_path

    def reModel(self):
        url ='http://127.0.0.1:6000/api/v0/ai/project/register'

        modelData = {
    #   // AI project name
                    "project": "SuperImageAI",
                    #   // List of AI model and HTTP interface information
                    "models": [
                        {
                        #   // Model name
                        "model": "superImage",
                        #   // HTTP Url for executing model
                        "api": "http://127.0.0.1:1088/v1/images/generations",
                        #   // Model type, default 0
                        #   // 0 - Text generation text model
                        #   // 1 - Text generation image model
                        #   // 2 - Image editing model
                        "type": 1
                        }
                    ]
                    }
        response = rt.post(url=url, json=modelData)

        r = response.json()
        
        registerResult = 0
        if r['code']==0:
            registerResult=1
        return registerResult 
        

    def read_register_status(self):
        file_path = self.config_file_path
        with open(file_path, 'r') as file:
            content = file.read()
            match = re.search(r'registerStatus\s*=\s*(\d+)', content)
            if match:
                return int(match.group(1))
            else:
                raise ValueError("registerStatus not found in the config file.")

    def write_register_status(self, new_status):
        file_path = self.config_file_path
        with open(file_path, 'r') as file:
            content = file.read()
        print("content=====",content,type(content))
        # new_content = re.sub(r'(registerStatus\s*=\s*)\d+', f'\\1{new_status}', content)
        new_content = 'registerStatus = {}'.format(new_status)

        with open(file_path, 'w') as file:
            file.write(new_content)

    def registerProcess(self):
        registerResult=self.reModel()
        if registerResult==1:
           self.write_register_status(1)
        else:
            self.write_register_status(0) 


# config_file_path = 'config.py'

# # 读取 registerStatus 的值
# current_status = read_register_status(config_file_path)
# print(f"Current registerStatus: {current_status}")

# # 修改 registerStatus 的值为 1 并保存
# write_register_status(config_file_path, 1)

# # 再次读取以确认修改
# new_status = read_register_status(config_file_path)
# print(f"New registerStatus: {new_status}")
