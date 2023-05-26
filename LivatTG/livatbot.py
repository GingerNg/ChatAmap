import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
print(os.path.dirname(os.getcwd()))

BotName = "LivatBot"
from utils.env_utils import init_custom_env
init_custom_env(flag="prod", botname=BotName)

from utils.logger_utils import get_logger
logger = get_logger()

from telegram import Update
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, \
                        InlineQueryHandler
from common.models.dao import FsaDao
from common.models.msgs import TgMsg, db, app
from utils.env_utils import tg_token, chat_id
from jobs import notion_agenda_job, rss_subscript_monitor_job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
fsa_dao = FsaDao(db=db, app=app)
from common.msg_svc import MsgSvc

svc = MsgSvc()

class Agent(object):
    def __init__(self) -> None:
        pass

# ******************** handlers ***************** #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(update.effective_chat.id)
    logger.info(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """清空当前用户的dialog history"""
    resp = svc.clear_history(role=update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)

async def text_msg_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == chat_id:
        resp = svc.pipeline(role=update.effective_chat.id, msg_text=update.message.text)
    else:
        resp = "unsupported user"
    # 保存文本
    # fsa_dao.save_obj(TgMsg(content=update.message.text, role=update.effective_chat.id, role_type="tg"))
    # fsa_dao.save_obj(TgMsg(content=update.message.text, role="livat_bot", role_type="tg"))
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(tg_token).build()

    # handlers
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), text_msg_save)
    start_handler = CommandHandler('start', start)
    clear_handler = CommandHandler('clear', clear)
    application.add_handler(start_handler)
    application.add_handler(clear_handler)
    application.add_handler(echo_handler)
    # application.add_handler(inline_caps_handler)

    # scheduler jobs
    scheduler = AsyncIOScheduler()
    trigger = IntervalTrigger(days=1, start_date='2023-04-14 10:00:00', weeks=0, end_date=None)
    scheduler.add_job(notion_agenda_job, trigger)

    trigger = IntervalTrigger(hours=4, start_date='2023-04-14 16:00:00', weeks=0, end_date=None)
    scheduler.add_job(rss_subscript_monitor_job, trigger)

    scheduler.start()

    # run
    application.run_polling()






