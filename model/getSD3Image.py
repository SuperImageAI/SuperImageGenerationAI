import websocket 
import uuid
import json
import urllib.request
import urllib.parse

class getSDImage:
    def __init__(self,server_address,rdata):

        self.rdata =rdata
        self.server_address=server_address
    # def queue_prompt(prompt):
    #     p = {"prompt": prompt, "client_id": client_id}
    #     data = json.dumps(p).encode('utf-8')
    #     req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    #     return json.loads(urllib.request.urlopen(req).read())

    def get_image(self,filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

    def get_history(self):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, self.rdata['prompt_id'])) as response:
            return json.loads(response.read())

    def get_images(self,ws):
        prompt_id = self.rdata['prompt_id']
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        images_output.append(image_data)
                output_images[node_id] = images_output

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