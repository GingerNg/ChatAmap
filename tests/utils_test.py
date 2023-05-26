from utils.gaode_utils import GaoDe
import logging
import yaml
from utils.rss_utils import fetch

def test_rss():
    print(fetch("https://kexue.fm/feed"))


def test_env():
    from utils.env_utils import env_conf
    print(env_conf)
    with open('conf/env.dev.yaml') as file:
        env_conf = yaml.safe_load(file)
        print(env_conf)


def test_logger():
    from utils.logger_utils import get_logger
    logger = get_logger()
    logger.error("test")
    logger = get_logger()
    logger.error("test2")


def test_openai():
    from utils.openai_utils import Openai
    openai_obj = Openai()
    messages =[
            {"role": "system", "content": "You are a writer, you are writing a story."},
            {"role": "user", "content": "你好"},
        ]
    resp = openai_obj.chat_complete(messages=messages, stream=False)
    print(resp)