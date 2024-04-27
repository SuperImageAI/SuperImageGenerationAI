from PIL import Image, ImageDraw, ImageFont

class addWaterMask:
    def __init__(self):
        self.font = ImageFont.truetype("/home/AI_project/superimage/font/KaTeX_Main-BoldItalic-70ee1f64.ttf",30)  # 选择字体和大小
        # self.font= ImageFont.load_default()
    def process(self, img, text):
        # img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        w,h = draw.textsize(text,self.font)
        position = (img.width-w-10, img.height-h-10) # 增加水印位置,
 
        draw.text(position, text, font=self.font, fill=(255,255,255))
        return img
 
 
addWM = addWaterMask()
