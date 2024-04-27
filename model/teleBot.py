import os

import telebot
import json
import requests as rt
import io
import base64
from PIL import Image
from sdModel import sdModel

from PIL import Image, ImageDraw, ImageFont
 
class addWaterMask:
    def __init__(self):
        self.font = ImageFont.truetype("/root/anaconda3/envs/sdwebui/lib/python3.10/site-packages/gradio/templates/cdn/assets/KaTeX_Main-BoldItalic-70ee1f64.ttf",30)  # 选择字体和大小
        # self.font= ImageFont.load_default()
    def process(self, img_path, text):
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        w,h = draw.textsize(text,self.font)
        position = (img.width-w-10, img.height-h-10) # 增加水印位置,
 
        draw.text(position, text, font=self.font, fill=(255,255,255))
        return img
 
 
test = addWaterMask()
# BOT_TOKEN = os.environ.get('6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo')

bot = telebot.TeleBot('6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo')
#bot = telebot.TeleBot('6926867064:AAEFCbBi3mw6Oip_shmNJXLtApDlujz8c2A')

    # bot.send_photo(image)

# app = ApplicationBuilder().token("6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "hello, how are you doing?")

@bot.message_handler(commands=['image'])
def send_welcome(message):
    bot.reply_to(message, "please Input your keyWords:")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    chat_id = message.chat.id
    
    print("=====flag0=====",chat_id,message.text)

    r = sdModel.sdImage(message.text)
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    # image.resize((10,10))
    print("=====flag1=====")
    imPath = '/home/AI_project/JupyterData/photos/'+str(chat_id)+'.png'
    image.save(imPath)
    water_mask = "SuperImageAI"
    image = test.process(imPath, water_mask)
 
    image.save(imPath)
    bot.send_photo(chat_id, photo=open(imPath, 'rb'))
    
if __name__ == "__main__":
    
    bot.infinity_polling(timeout=60, long_polling_timeout = 60)

