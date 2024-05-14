from PIL import Image, ImageDraw, ImageFont
import os
current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# print(parent_dir)
class addWaterMask:
    def __init__(self):
        current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        # print(parent_dir)
        self.font = ImageFont.truetype(current_dir+"/font/KaTeX_Main-BoldItalic-70ee1f64.ttf",30)  # 选择字体和大小
        # self.font= ImageFont.load_default()
    def process(self, img, text):
        # img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        w,h = draw.textsize(text,self.font)
        position = (img.width-w-10, img.height-h-10) # 增加水印位置,
 
        draw.text(position, text, font=self.font, fill=(255,255,255))
        return img
 
 
addWM = addWaterMask()
