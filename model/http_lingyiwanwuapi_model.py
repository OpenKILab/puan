import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
from openai.types.chat import ChatCompletion

from loguru import logger

class LingyiwanwuAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        API_BASE = "https://api.lingyiwanwu.com/v1"
        API_KEY = "c883e7b05af94f89b2c7b4bbe98ae867"
        self.client = OpenAI(
            api_key=API_KEY,
            base_url=API_BASE
        )


    def generate(self, prompt, messages=None, *args, **kwargs):
        try:
            completion = self.client.chat.completions.create(
                model="yi-large",
                messages=[{"role": "user", "content": prompt}]
            )
        except Exception as e:
            return e

        return completion

    def parse(self, response):
        logger.debug(response)
        if isinstance(response, ChatCompletion):
            return (
                True,
                response.choices[0].message.content,
            )
        else:
            return(
                False,
                str(response)
            )
