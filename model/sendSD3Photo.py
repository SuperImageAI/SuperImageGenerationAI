from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import requests
from PIL import Image
import requests
from io import BytesIO
from sdModel import sdModel
import io
import os
import base64
from addWaterMask import addWM
from SD3Client import SD3Client


# TOKEN = '6926867064:AAEFCbBi3mw6Oip_shmNJXLtApDlujz8c2A'
TOKEN = '6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo'

# API_URL = 'YOUR_BACKEND_API_URL'  # 假设的后端API，根据文本生成四张图片的URL

# 开始命令的处理器
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('发送文本生成图片。')

# 处理文本消息，生成图片
async def generate_images(update: Update, context: CallbackContext):
    text = update.message.text

    images =[]
    server_adresses = [
        "127.0.0.1:8188",
        "127.0.0.1:8189"
    ]
    # client_id = str(uuid.uuid4())
    client = SD3Client(server_adresses)
    images = await client.fetch_images(text)
    print("=================flag1============",len(images))    

    if len(images) == 4:
    # 确保所有图片大小相同（这里以第一张图片的大小为准）
        width, height = images[0].size
        total_width = width * 2
        total_height = height * 2

        # 创建一个新的、足够大的图片来容纳所有小图片
        new_im = Image.new('RGB', (total_width, total_height))

        # 将四张图片粘贴到这个新图片上
        new_im.paste(images[0], (0,0))
        new_im.paste(images[1], (width,0))
        new_im.paste(images[2], (0,height))
        new_im.paste(images[3], (width,height))
        # 保存或显示这个新图片
        current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        imPath = parent_dir+'/photos/'+str(update.effective_chat.id)+'combined.jpg'
        new_im.save(imPath)

        await context.bot.send_photo(update.effective_chat.id,open(imPath,'rb'))

        image1Path=parent_dir+'/photos/'+str(update.effective_chat.id)+'image1.jpg'
        image2Path=parent_dir+'/photos/'+str(update.effective_chat.id)+'image2.jpg'
        image3Path=parent_dir+'/photos/'+str(update.effective_chat.id)+'image3.jpg'
        image4Path=parent_dir+'/photos/'+str(update.effective_chat.id)+'image4.jpg'
        images[0].save(image1Path)
        images[1].save(image2Path)
        images[2].save(image3Path)
        images[3].save(image4Path)
    # await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
    # 发送选择按钮
        keyboard = [[InlineKeyboardButton(f"Image {i+1}", callback_data=str(i)) for i in range(4)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Choose the one you like best：', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Failed to generate image。')

# 处理按钮回调
async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    # 这里可以根据callback_data处理用户的选择
    selected_image_index = query.data
    await query.edit_message_text(f'You selected Image {int(selected_image_index)+1}')
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    selectImPath =parent_dir+'/photos/'+str(update.effective_chat.id)+'image' +str(int(selected_image_index)+1)+'.jpg'
    await context.bot.send_photo(update.effective_chat.id,open(selectImPath,'rb'))

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(MessageHandler(filters.COMMAND, generate_images))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == '__main__':
    main()
