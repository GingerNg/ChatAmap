import os
import openai

openai.api_base = os.environ["OPENAI_API_BASE"]
openai.api_key = os.environ["OPENAI_API_KEY"]

from utils.logger_utils import get_logger
logger = get_logger()

class Openai(object):
    @staticmethod
    def chat_complete(messages, stream=True):
        """
        Call OpenAI Chat Completion API with text prompt.
        """
        kwargs = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "timeout": 5,
            "stream": stream,
            "presence_penalty": 1,
            # "max_tokens": 800,
            "temperature": 0.8
        }
        try:
            response = openai.ChatCompletion.create(**kwargs)
            # return response["choices"][0]["message"]['content']
            return response
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
