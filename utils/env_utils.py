import yaml
import os
root_dir = os.path.dirname(os.path.dirname(__file__))
# print(root_dir)
from utils.logger_utils import init_logger


env_conf = None
default_env_conf = None

# db
db_url = None

# notion
notion_token = None
notion_db_id = None
# tg
tg_token = None
chat_id = None
channel_chat_id = None
group_chat_id = None
shanbay_cookie = None

gaode_key = None

opena_api_base = None

def init_default_env(flag="prod"):
    """
    默认环境变量
    """
    if flag == "dev":
        pth = f'{root_dir}/conf/env.dev.yaml'
    else:
        pth = f'{root_dir}/conf/env.yaml'
    with open(pth, 'r') as file:
        default_env_conf = yaml.safe_load(file)
    global notion_token, notion_db_id, \
            shanbay_cookie, gaode_key, opena_api_base
    import os
    os.environ["OPENAI_API_KEY"] = default_env_conf["openai"]["token"]
    os.environ["OPENAI_API_BASE"] = default_env_conf["openai"]["apiBase"]

    notion_token = default_env_conf["notion"]["token"]
    notion_db_id = default_env_conf["notion"]["dbId"]["agenda2"]

    shanbay_cookie = default_env_conf["shanbay"]["cookie"]

    gaode_key = default_env_conf["gaode"]["key"]


init_default_env()


def init_custom_env(flag="prod", botname="LivatBot"):
    """
    自定义环境变量
    """
    init_logger(file_name=botname, name=botname)
    if flag == "dev":
        pth = f'{root_dir}/conf/env.dev.yaml'
    else:
        pth = f'{root_dir}/conf/env.yaml'
    global env_conf, channel_chat_id, group_chat_id, notion_token, notion_db_id, chat_id, tg_token, db_url
    if env_conf is None:
        with open(pth, 'r') as file:
            env_conf = yaml.safe_load(file)

            bots = env_conf["tg"]["bots"]
            tg_token = bots[botname]["token"]

            chat_id = env_conf["tg"]["chatId"]['userId']

            channel_chat_id = env_conf["tg"]["chatId"]["channelId"]["testChannel"]
            group_chat_id = env_conf["tg"]["chatId"]["groupId"]["testGroup"]
            # db_type = env_conf["db"]["type"]
            db_url = env_conf["db"]["url"] = f"sqlite:///{botname}.sqlite3"





