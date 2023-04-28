import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
# os.path.dirname(os.getcwd()))

BotNanme = "TranslatorBot"
from utils.env_utils import init_custom_env, root_dir
init_custom_env(flag="prod", botname=BotNanme)
from utils.logger_utils import get_logger
logger = get_logger()

from telegram import Update
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, \
                        InlineQueryHandler
from common.models.dao import FsaDao, TranslatorBotMsgDao
from common.models.msgs import db, app, TranslatorBotMsg
from utils.env_utils import tg_token

from shanbay import pipeline
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
fsa_dao = FsaDao(db=db, app=app)
botmsg_dao = TranslatorBotMsgDao(db=db, app=app)


class Agent(object):
    def __init__(self) -> None:
        pass

import time
# ******************** handlers ***************** #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.id)
    print(update.message.text)
    msg = "Hello, I'm TranslatorBot, I can translate English to Chinese, and Chinese to English."
    # await send_typing_message(update, context, msg)
    # await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

from utils.lang_utils import translate
async def text_msg_translate_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 保存文本
    fsa_dao.save_obj(TranslatorBotMsg(content=update.message.text, role=update.effective_chat.id, role_type="tg"))
    res = translate(update.message.text)
    if res:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=res)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="translate failed")

from utils.trans_text_audio import edge_tts
async def text2voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        item = botmsg_dao.fetch(limit=1)[0]
        voice_pth = f"{root_dir}/data/{item.content}.mp3"
        edge_tts(text=item.content, voice_pth=voice_pth)
        with open(voice_pth, 'rb') as audio:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=audio)
    except Exception as e:
        logger.error(e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"text2voice failed {e}")



if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_token).build()

    # handlers
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), text_msg_translate_save)
    start_handler = CommandHandler('start', start)
    text2voice_handler = CommandHandler('text2voice', text2voice)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(text2voice_handler)

    # scheduler jobs
    scheduler = AsyncIOScheduler()
    trigger = IntervalTrigger(days=1, start_date='2023-04-26 19:15:00', weeks=0, end_date=None)
    scheduler.add_job(pipeline, trigger)

    scheduler.start()
    # run
    application.run_polling()