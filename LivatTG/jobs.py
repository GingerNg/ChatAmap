
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import telegram
import asyncio
from utils.env_utils import tg_token, chat_id
bot = telegram.Bot(token=tg_token)

from utils.datetime_utils import move_now, timestr2datetime
from utils.notion_utils import get_rows
from utils.rss_utils import fetch
from common.models.dao import RssMsgDao
from common.models.msgs import RssMsg, db, app
from utils.logger_utils import get_logger
logger = get_logger()

def get_content():
    try:
        # today = move_now(0, fm='%Y-%m-%d')
        yesterday = move_now(-1, fm='%Y-%m-%d')
        tomorrow  = move_now(1, fm='%Y-%m-%d')
        resp = get_rows(start=yesterday, end=tomorrow)
        # print(resp)
        content = """
        tasks in notion:
        """
        for row in resp["results"]:
            content += row["properties"]["Task"]["title"][0]["text"]["content"]
            content += "\n"
        return content
    except Exception as e:
        logger.error(e)
        return "get_notion_content_error"

# async def main():
#     async with bot:
#         await bot.send_message(text=get_content(), chat_id=chat_id)

async def main():
    async with bot:
        logger.debug((await bot.get_updates())[0])

# ******************************************** jobs
async def notion_agenda_job():
    async with bot:
        await bot.send_message(text=get_content(), chat_id=chat_id)


rss_msg_dao = RssMsgDao(db=db, app=app)
async def rss_subscript_monitor_job():
    rss_urls = {
    # "TechCrunch-startups": 'https://feeds.feedburner.com/TechCrunch/startups',
    # "捕🐍者说": "https://pythonhunter.org/episodes/feed.xml",
    "栋哥的赛博空间": "https://liuyandong.com/feed",
    "品橙旅游": "https://www.pinchain.com/feed",
    "阮一峰的网络日志": "https://www.ruanyifeng.com/blog/atom.xml",
    "月光博客": "https://www.williamlong.info/rss.xml",
    "FindHao": "https://www.findhao.net/feed.xml",
    "科学空间|Scientific Spaces": "https://kexue.fm/feed",
    }

    for source, rss_url in rss_urls.items():
        new_items = []
        try:
            items = fetch(rss_url=rss_url)
            # print(items)
            for item in items:
                obj = RssMsg(source=source, title=item["Title"], link=item["Link"], summary=item["Summary"], published=timestr2datetime(item["Published"]))
                if rss_msg_dao.insert(obj):
                    new_items.append(item)
            # print(new_list)
            for item in new_items:
                content = ""
                for k,v in item.items():
                    if k != "Summary":
                        content += f"{k}: {v}"
                        content += "\n"
                async with bot:
                    await bot.send_message(text=content, chat_id=chat_id)
        except Exception as e:
            logger.error(e)
            async with bot:
                await bot.send_message(text=f"{source}: get_rss_content_error", chat_id=chat_id)


# ********************************************

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# scheduler = AsyncIOScheduler()
# trigger = IntervalTrigger(days=1, start_date='2023-04-14 10:00:00', weeks=0, end_date=None)
# scheduler.add_job(send_message, trigger)
# scheduler.start()

# loop = asyncio.get_event_loop()
# loop.run_forever()


if __name__ == '__main__':
    asyncio.run(rss_subscript_monitor_job())