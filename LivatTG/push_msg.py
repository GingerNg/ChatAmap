import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
print(os.path.dirname(os.getcwd()))

from utils.env_utils import init_custom_env
init_custom_env(flag="dev", botname="TestLivat")

from utils.env_utils import tg_token, channel_chat_id, chat_id, group_chat_id
import telegram
import asyncio

bot = telegram.Bot(tg_token)

async def get_chat_id():
    """获取chat_id and me"""
    async with bot:
        # print((await bot.get_updates())[-1])
        print(await bot.get_me()) # 获取当前bot的信息

async def send_msg(content, chat_id):
    async with bot:
        await bot.send_message(text=content, chat_id=chat_id)

async def send_voice(chat_id):
    async with bot:
        with open('/***/***/story.mp3', 'rb') as audio:
            await bot.send_voice(chat_id=chat_id, voice=audio)

# Define the menu options
menu_buttons = [
    [telegram.KeyboardButton("Option 1")],
    [telegram.KeyboardButton("Option 2")],
    [telegram.KeyboardButton("Option 3")]
]

# Create the menu markup
menu_keyboard = telegram.ReplyKeyboardMarkup(menu_buttons, resize_keyboard=False)

from telegram.ext import CommandHandler

# define a function to handle the command
def menu_command(update, context):
    # create list of options
    options = ['Option 1', 'Option 2', 'Option 3']
    # send menu to user
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Please select an option:',
                             reply_markup=telegram.ReplyKeyboardMarkup([options], resize_keyboard=True))

# async def send_menu():
#     async with bot:
#         # Send the menu to the user
#         await bot.send_message(chat_id=chat_id, text="Please select an option:", reply_markup=menu_keyboard)

if __name__ == '__main__':

    # asyncio.run(send_menu())

    # asyncio.run(send_voice(chat_id))

    # bot往channel发消息, 当bot被移除channel时，会报错
    # asyncio.run(send_msg("1212", Channel_chat_id))

    # bot 往group发消息
    # asyncio.run(send_msg("1212", group_chat_id))