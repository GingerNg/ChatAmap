import re
from common.handlers import GPT35ApiInference
from common.models.dto import UniMsg
from utils.logger_utils import get_logger
logger = get_logger()

user_history = {} # key: role/user_id, value: history[] todo

def is_link(text):
    """
    该正则表达式匹配标准的URL格式。如果给定文本是一个URL，则返回True，否则返回False。
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http://, https://, ftp://, ftps://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or IP
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, text) is not None


class MsgSvc(object):
    def __init__(self) -> None:
        self.inference = GPT35ApiInference()

    def clear_history(self, role: str):
        """
        清空历史消息
        """
        user_history[role] = []
        return "cleared"

    def pipeline(self, role: str, msg_text: str):
        """
        消息处理服务
        """
        if is_link(msg_text):
            return "saved"
        else:
            logger.debug(user_history)
            history = user_history.get(role, [])
            history.append(UniMsg(content=msg_text, round=len(history), role_type="user"))
            # todo save to db
            resp = self.inference.infer(history=history)
            history.append(UniMsg(content=resp, round=len(history), role_type="system"))
            user_history[role] = history
            return resp

if __name__ == "__main__":
    print(is_link("https://www.baidu.com dsdsds"))