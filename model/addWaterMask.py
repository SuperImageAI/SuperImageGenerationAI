from PIL import Image, ImageDraw, ImageFont
import os
current_dir =  os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# print(parent_dir)
class addWaterMask:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        print(current_dir)
        # current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        print(parent_dir,current_dir)
        self.font = ImageFont.truetype(parent_dir+"/font/KaTeX_Main-BoldItalic-70ee1f64.ttf",30)  # 选择字体和大小
        # self.font= ImageFont.load_default()
    def process(self, img, text):
        # img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0,0),text,self.font)
        w,h =bbox[2] - bbox[0], bbox[3] - bbox[1]
        position = (img.width-w-10, img.height-h-10) # 增加水印位置,
 
        draw.text(position, text, font=self.font, fill=(255,255,255))
        return img
 
 
addWM = addWaterMask()
