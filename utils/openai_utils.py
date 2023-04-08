import os
import openai
from . import env
from .logger_utils import logging

import os
os.environ["OPENAI_API_KEY"] = env.openai_api_key

openai.api_base = env.openai_api_base
openai.api_key = os.environ["OPENAI_API_KEY"]

class Openai:
    """OpenAI Connector."""

    @staticmethod
    def chat_complete(messages, stream=True):
        kwargs = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "timeout": 5,
            "stream": stream,
            "presence_penalty": 1,
            "temperature": 0.8
        }
        try:
            response = openai.ChatCompletion.create(**kwargs)
            return response
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return e


