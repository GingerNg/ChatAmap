from utils.openai_utils import Openai
from utils.logger_utils import get_logger
from typing import List
from common.models.dto import UniMsg
logger = get_logger()

class GPT35ApiInference(object):
    def __init__(self) -> None:
        self.openai_obj = Openai()

    @staticmethod
    def build_messages(history:List[UniMsg], syetem_role_content):
        messages = []
        if syetem_role_content:
            messages.append({"role": "system", "content": syetem_role_content})
        for h in history:
            messages.append({"role": h.role_type, "content": h.content})
        return messages

    def infer(self, history:List[UniMsg], stream=False, syetem_role_content="You are a helpful assisant"):
        try:

            messages = self.build_messages(history=history, syetem_role_content=syetem_role_content)
            logger.debug(messages)
            response = self.openai_obj.chat_complete(messages, stream=stream)
            logger.debug(response)
            return response
        except Exception as e:
            logger.error(e)

