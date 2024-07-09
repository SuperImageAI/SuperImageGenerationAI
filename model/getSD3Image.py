import websocket 
import uuid
import json
import requests as rt

class getSDImage:
    def __init__(self,server_address,client_id,rdata):
        self.server_address=server_address
        self.client_id = client_id
        self.rdata =rdata

    # def queue_prompt(prompt):
    #     p = {"prompt": prompt, "client_id": client_id}
    #     data = json.dumps(p).encode('utf-8')
    #     req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    #     return json.loads(urllib.request.urlopen(req).read())

    def get_image(self,filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        response = rt.get(f"http://{self.server_address}/view", params=data)
        return response.content

    def get_history(self,prompt_id):
        response = rt.get(f"http://{self.server_address}/history/{prompt_id}")
        return response.json()

    def get_images(self):
        prompt_id = self.rdata['prompt_id']
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        # output_images = {}
        print("flag====",prompt_id,self.rdata)
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                print("flagxxxxx====",message['type'])
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
                elif message['type'] == 'status' :
                     flag = message['data']['status']['exec_info']['queue_remaining']  
                     if flag ==0: 
                        break
            else:
                continue #previews are binary data
        history =  self.get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        images_output.append(image_data)
                    # output_images[node_id] = images_output
 
        return image_data


    # with open("workflow_api.json","r",encoding="utf-8") as f:
    #     workflow_jsondata = f.read()

    # prompt = json.loads(workflow_jsondata)
    # # prompt = json.loads(prompt_text)
    # #set the text prompt for our positive CLIPTextEncode
    # prompt["6"]["inputs"]["text"] = "masterpiece best quality man"

    # #set the seed for our KSampler node
    # prompt["3"]["inputs"]["seed"] = 5

    # ws = websocket.WebSocket()
    # ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    # images = get_images(ws, prompt)