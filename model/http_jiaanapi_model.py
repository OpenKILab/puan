import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class JiaanAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://h5.ruyisheng.com/gateway/common/v3/paste.htm?devid=63106113405667&mc=2000&source=55&uid=629572282&verifyCode=827e7fd9d40539f5876ff9687d4ffb17&version=1.1.23.9'
        self.headers = {
            "Content-Type": "application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]

        data = {
            "content": prompt,
            "isKouLing": 0
        }
        
        try:
            response = requests.post(self.url, data=data, headers=self.headers)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()['data']['toast'],
            )
        else:
            return(
                False,
                ""
            )
