import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
print(os.path.dirname(os.getcwd()))

from utils.env_utils import init_custom_env
init_custom_env(flag="dev", botname="TestLivat")
from utils.env_utils import tg_token

from telegram import Update
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, \
                        InlineQueryHandler

import asyncio

async def print_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("----")
    print(update.message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="saved")
    # 保存文本
    # fsa_dao.save_obj(TgMsg(content=update.message.text, role=update.effective_chat.id, role_type="tg"))
    # fsa_dao.save_obj(TgMsg(content=update.message.text, role="livat_bot", role_type="tg"))
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="saved")

if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_token).build()

    # handlers
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    echo_handler = MessageHandler(~filters.COMMAND, print_msg)

    application.add_handler(echo_handler)
    application.run_polling()