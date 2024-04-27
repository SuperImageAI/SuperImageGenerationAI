import os
import telebot
import json
import requests as rt
import io
import base64
from PIL import Image
# from tranModel import trmodel
from sdModel import sdModel
import torch
import torchaudio
from seamless_communication.inference import Translator
# BOT_TOKEN = os.environ.get('6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo')
from PIL import Image, ImageDraw, ImageFont
 
class addWaterMask:
    def __init__(self):
        self.font = ImageFont.truetype("/home/AI_project/superimage/font/KaTeX_Main-BoldItalic-70ee1f64.ttf",30)  # 选择字体和大小
        # self.font= ImageFont.load_default()
    def process(self, img_path, text):
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        w,h = draw.textsize(text,self.font)
        position = (img.width-w-10, img.height-h-10) # 增加水印位置,
 
        draw.text(position, text, font=self.font, fill=(255,255,255))
        return img
 
 
test = addWaterMask()
Koreabot = telebot.TeleBot('6325213038:AAFpUpJXFoFyWrffLSvK6OZHVzkkdEuJa0I')


translator =  Translator(
       model_name_or_card="seamlessM4T_large",
       vocoder_name_or_card="vocoder_36langs",
        device=torch.device("cuda:2"),
       dtype= torch.float16,
        apply_mintox=False
       )

    # bot.send_photo(image)

# app = ApplicationBuilder().token("6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()

@Koreabot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    Koreabot.reply_to(message, "hello, how are you doing?")

@Koreabot.message_handler(commands=['image'])
def send_welcome(message):
    Koreabot.reply_to(message, "please Input your keyWords:")


@Koreabot.message_handler(func=lambda msg: True)
def echo_all(message):
    chat_id = message.chat.id
    
    print("=====flag0=====",chat_id,message.text)
    translated_text, _ = translator.predict(message.text, "t2tt", 'eng', 'kor')

    # translated_text = trmodel.tranPredict(message.text, "t2tt", 'eng', 'kor')
    print("=====flag1=====",translated_text)
    r = sdModel.sdImage(str(translated_text))
    
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    # image.resize((10,10))
  
    imPath = '/home/AI_project/JupyterData/photos/'+str(chat_id)+'.png'
    image.save(imPath)
    water_mask = "SuperImageAI"
    image = test.process(imPath, water_mask)
 
    image.save(imPath)
    Koreabot.send_photo(chat_id, photo=open(imPath, 'rb'))
if __name__ == "__main__":
    
    Koreabot.infinity_polling()
