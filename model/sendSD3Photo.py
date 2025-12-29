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
import logging
from telegram.error import BadRequest, NetworkError, TimedOut


# TOKEN = '6926867064:AAEFCbBi3mw6Oip_shmNJXLtApDlujz8c2A'
# TOKEN = '6425101277:AAGQ7w2W74-ks1PV1BQ_-CXi5IS9On_QQHo'
TOKEN = '8472024095:AAG34uPfB88E_B-S6ucLlKTC9YC4WCU97iY'

# API_URL = 'YOUR_BACKEND_API_URL'  # 假设的后端API，根据文本生成四张图片的URL

# 开始命令的处理器
async def start(update: Update, context: CallbackContext):
    user_info = f"User: {update.effective_user.username} ({update.effective_user.id})"
    print(f"[START] {user_info} started the bot")
    try:
        if update.message:
            await update.message.reply_text('Bot started! Send text to generate images.')
        else:
            await context.bot.send_message(update.effective_chat.id, 'Bot started! Send text to generate images.')
    except (BadRequest, NetworkError, TimedOut) as e:
        print(f"[ERROR] Failed to send start message: {e}")

# 处理文本消息，生成图片
async def generate_images(update: Update, context: CallbackContext, text: str):
    user_info = f"User: {update.effective_user.username} ({update.effective_user.id})"
    print(f"[GENERATE] {user_info} requested image generation")
    print(f"[PROMPT] Text: '{text}'")

    images = []
    server_adresses = [
        "8.219.75.114:8081"
    ]
    client = SD3Client(server_adresses)
    print(f"[SD3] Starting image generation with prompt: {text}")
    images = await client.fetch_images(text)
    print(f"[SD3] Generated {len(images)} images")
  

    if len(images) == 4:
        print(f"[SUCCESS] 4 images generated successfully, creating combined image")
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
        os.makedirs(parent_dir + '/photos', exist_ok=True)  # 确保目录存在
        imPath = parent_dir+'/photos/'+str(update.effective_chat.id)+'combined.jpg'
        new_im.save(imPath)

        print(f"[SEND] Sending combined image to {user_info}")
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
        print(f"[UI] Showing selection buttons to {user_info}")
        try:
            if update.message:
                await update.message.reply_text('Choose the one you like best:', reply_markup=reply_markup)
            else:
                await context.bot.send_message(update.effective_chat.id, 'Choose the one you like best:', reply_markup=reply_markup)
        except BadRequest as e:
            print(f"[WARNING] Could not reply to message (may have been deleted): {e}")
            # 尝试直接发送消息而不回复
            try:
                await context.bot.send_message(update.effective_chat.id, 'Choose the one you like best:', reply_markup=reply_markup)
            except Exception as e2:
                print(f"[ERROR] Failed to send selection message: {e2}")
    else:
        print(f"[ERROR] Image generation failed for {user_info}, got {len(images)} images instead of 4")
        try:
            if update.message:
                await update.message.reply_text('Failed to generate images. Please try again later.')
            else:
                await context.bot.send_message(update.effective_chat.id, 'Failed to generate images. Please try again later.')
        except (BadRequest, NetworkError, TimedOut) as e:
            print(f"[ERROR] Failed to send error message: {e}")

# 处理按钮回调
async def button_callback(update: Update, context: CallbackContext) -> None:
    user_info = f"User: {update.effective_user.username} ({update.effective_user.id})"
    query = update.callback_query
    await query.answer()
    # 这里可以根据callback_data处理用户的选择
    selected_image_index = query.data
    print(f"[SELECTION] {user_info} selected Image {int(selected_image_index)+1}")
    try:
        await query.edit_message_text(f'You selected Image {int(selected_image_index)+1}')
    except Exception as e:
        print(f"[WARNING] Could not edit message: {e}")
        await query.answer(f'You selected Image {int(selected_image_index)+1}')
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    selectImPath =parent_dir+'/photos/'+str(update.effective_chat.id)+'image' +str(int(selected_image_index)+1)+'.jpg'
    print(f"[SEND] Sending selected image {int(selected_image_index)+1} to {user_info}")
    await context.bot.send_photo(update.effective_chat.id,open(selectImPath,'rb'))
async def custom_command_handler(update: Update, context: CallbackContext):
    user_info = f"User: {update.effective_user.username} ({update.effective_user.id})"
    
    # 检查 update.message 是否存在
    if not update.message or not update.message.text:
        print(f"[IGNORE] {user_info} sent message without text (may be edit/delete), ignoring")
        return
    
    text = update.message.text
    print(f"[MESSAGE] {user_info} sent: '{text}'")

    if text.startswith('/'):  # 检查是否以 "/" 开头
        # 将命令前缀去掉，直接提取文本内容
        command = text[1:].strip()  # 去掉 "/" 并去掉多余的空格
        if command:  # 如果命令非空，直接将其作为文本传递给图像生成逻辑
            print(f"[COMMAND] {user_info} used command: /{command}")
            await generate_images(update, context, command)  # 调用图像生成逻辑并传递解析后的文本
        else:
            print(f"[ERROR] {user_info} sent empty command")
            try:
                await update.message.reply_text("Command is empty. Please provide text after '/'.")
            except (BadRequest, NetworkError, TimedOut) as e:
                print(f"[ERROR] Failed to send error message: {e}")
    else:
        # 如果消息不以 "/" 开头，不做任何反应
        print(f"[IGNORE] {user_info} sent non-command message, ignoring")
        pass

# 全局错误处理器
async def error_handler(update: object, context: CallbackContext) -> None:
    """处理所有未捕获的异常"""
    error = context.error
    print(f"[ERROR HANDLER] Exception while handling an update: {error}")
    
    # 记录不同类型的错误
    if isinstance(error, BadRequest):
        print(f"[ERROR] BadRequest: {error}")
    elif isinstance(error, NetworkError):
        print(f"[ERROR] NetworkError: {error}")
    elif isinstance(error, TimedOut):
        print(f"[ERROR] TimedOut: {error}")
    else:
        print(f"[ERROR] Unexpected error: {type(error).__name__}: {error}")
    
    # 尝试向用户发送错误消息（如果可能）
    if update and isinstance(update, Update):
        try:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="抱歉，处理您的请求时出现了错误。请稍后再试。"
                )
        except Exception as e:
            print(f"[ERROR] Failed to send error message to user: {e}")

# 主函数
def main():
    print("=" * 50)
    print("🤖 SuperImageGenerationAI Bot Starting...")
    print(f"Bot Token: {TOKEN[:20]}...")
    print("=" * 50)

    application = Application.builder().token(TOKEN).build()

    # 禁用自动删除webhook
    application.updater.bootstrap_retries = 0

    # 添加全局错误处理器
    application.add_error_handler(error_handler)

    # 添加命令处理器
    application.add_handler(CommandHandler('start', start))

    # 添加自定义命令解析处理器
    application.add_handler(MessageHandler(filters.TEXT, custom_command_handler))

    # 添加按钮回调处理器
    application.add_handler(CallbackQueryHandler(button_callback))

    print("🚀 Bot is running and waiting for messages...")
    print("Press Ctrl+C to stop the bot")
    print("=" * 50)

    application.run_polling()

if __name__ == '__main__':
    main()
