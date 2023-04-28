
import asyncio
from utils.env_utils import init_custom_env
init_custom_env()
from utils.logger_utils import get_logger
logging = get_logger()
from utils.notion_utils import get_rows
from utils.datetime_utils import move_now, timestr2datetime
from LivatTG.jobs import notion_agenda_job

def test_notion_fetch():
    yesterday = move_now(-1, fm='%Y-%m-%d')
    tomorrow  = move_now(1, fm='%Y-%m-%d')
    resp = get_rows(start=yesterday, end=tomorrow)
    logging.info(resp)


async def test_notion_agenda2_job():
    asyncio.run(notion_agenda_job())

# def test_tts_edge():
#     from LivatTG.shanbay import story_tts
#     story_tts(story="hello wold", article_name="test.mp3")


# def test_shanbay_pipeline():
#     from LivatTG.shanbay import pipeline
#     asyncio.run(pipeline())